# uvicorn server_for_app.main:app --reload 
# http://localhost:8000
# http://localhost:8000/docs

import csv
from datetime import datetime
from models import User, Climate
from loggers import logger
from fastapi import FastAPI
import os.path
from environs import Env
import pandas as pd
import logging

app = FastAPI()

env = Env()  # Создаем экземпляр класса Env
env.read_env(r'C:\Users\vbekr\OneDrive\Рабочий стол\Python\server_for_app\inter.env') # Методом read_env() читаем файл .env и загружаем из него переменные в окружение
# env.read_env('inter.env')
user = env('user')

logger = logging.getLogger(__name__)

logger.propagate = False  # Что бы логи root не дублировались

@app.post("/setdata/")
async def climate_data(cl: Climate): 
    '''Хендлер для записи данных Climate в файл data.csv
    Запрос должен приходить в виде JSON файла'''  
    
    logger.info('Принимаем данные от пользователя!')

    if not os.path.exists('data.csv'):
        exists_csv = True
    else:
        exists_csv = False

    with open('data.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        if exists_csv:
            writer.writerow(['humidity', 'temperature', "room", "login", 'date'])
        writer.writerow([cl.humidity, cl.temperature, cl.room, cl.login, cl.creation_date])
        logger.info('Файл data.csv изменён!')
    
    try:
        df_new = pd.read_csv('data.csv')

        GFG = pd.ExcelWriter('data.xlsx')
        df_new.to_excel(GFG,  sheet_name='Климатика', index=False)
        GFG._save()

        logger.info('Файл data.xlsx изменён!')
    except Exception as e:
        logger.error(f'{e}')

    return {"humidity": cl.humidity, "temperature": cl.temperature, "room": cl.room, "login": cl.login,"creation_date": cl.creation_date}

@app.get("/hello/")
async def get_hello():
    """Хэндлер для проверки соединения с клиентом"""
    try:
        return {'Hello client'}
    except Exception as e:
        logger.error(f'{e}')

@app.get("/avt/")
async def avt(login, password):
    """Хэндлер для аутентификации"""
    logger.info('Аутентификация')
    if login in user:
        if password == user[login]:
            logger.info(f'Пользователь {login} аутентифицирован')
            return True
    else:
        return False
    
@app.get("/for_info/")
async def for_info(room):
    """Хэндлер для проверки актуальности полученных данных"""
    try:
        with open('data.csv', encoding='utf-8') as file:
            rows = csv.DictReader(file)
            return {max(datetime.fromisoformat(row['date']) for row in rows if row['room'] == room)}
    except Exception as e:
        logger.error(f'{e}')
 