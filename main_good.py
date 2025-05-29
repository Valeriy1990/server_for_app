# uvicorn server_for_app.main:app --reload 
# http://localhost:8000
# http://localhost:8000/docs

import csv
from datetime import datetime
from models import User, Climate
from loggers import logger
from fastapi import FastAPI
import uvicorn
import logging
import sys
from environs import Env
import os.path

import pandas as pd

app = FastAPI()

logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter('--> [%(levelname)-8s] - [Line %(lineno)d : def %(funcName)s : %(filename)s] - %(message)s'))
logger.addHandler(stdout_handler)

user = {'Valeriy': '1111'}

@app.post("/setdata/")
async def climate_data(cl: Climate): 
    '''Хендлер для записи данных Climate в файл data.csv
    Запрос должен приходить в виде JSON файла'''  
    
    logger.info('Принимает данные с клиента!')

    if not os.path.exists('data.csv'):
        exists_csv = True
    else:
        exists_csv = False

    with open('data.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        if exists_csv:
            writer.writerow(['humidity', 'temperature', "room", "login", 'date'])
        writer.writerow([cl.humidity, cl.temperature, cl.room, cl.login, cl.creation_date])
        logger.info('Запись в data.csv прошла успешно!')
    
    # Reading the csv file
    df_new = pd.read_csv('data.csv')

    # saving xlsx file
    GFG = pd.ExcelWriter('data.xlsx')
    df_new.to_excel(GFG,  sheet_name='Климатика', index=False)
    GFG._save()

    logger.info('Запись в .xlsx прошла успешно!')

    return {"humidity": cl.humidity, "temperature": cl.temperature, "room": cl.room, "login": cl.login,"creation_date": cl.creation_date}

@app.get("/hello/")
async def get_hello():
    """Хэндлер для проверки соединения с клиентом"""
    logger.info('Связь с клиентом!')
    return {'Hello client'}

@app.get("/avt/")
async def avt(login, password):
    """Хэндлер для аутентификации"""
    logger.info('Аутентификация!')
    if login in user:
        if password == user[login]:
            return True
    else:
        return False
    
@app.get("/for_info/")
async def for_info(room):
    """Хэндлер для проверки актуальности полученных данных"""
    logger.info('Сработал хендлер for_info!')
    with open('data.csv', encoding='utf-8') as file:
        rows = csv.DictReader(file)
        return {max(datetime.fromisoformat(row['date']) for row in rows if row['room'] == room)}



if __name__ == "__main__":
    uvicorn.run('main:app', host='192.168.1.33', port=8066, reload=True)
    # uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
    # uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)