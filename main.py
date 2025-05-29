# uvicorn server_for_app.main:app --reload 
# http://localhost:8000
# http://localhost:8000/docs

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import BoxShadow, Color

import csv
from datetime import datetime
from models import User, Climate
from loggers import logger
import uvicorn
from fastapi import FastAPI
import logging
import sys
# from environs import Env
import os.path
from multiprocessing import Process
import pandas as pd

app = FastAPI()

logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter('--> [%(levelname)-8s] - [Line %(lineno)d : def %(funcName)s : %(filename)s] - %(message)s'))
logger.addHandler(stdout_handler)

user = {'Valeriy': '1111'}

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_text = ""

    def for_log(self, message):
        self.log_text += message + "\n"
        if hasattr(self, 'log_label'):
            self.log_label.text = self.log_text

    def build(self):
        self.label = Label(text="Сервер запущен")
        self.log_label = Label(text="", size_hint_y=None, height=200)
        layout = BoxLayout(orientation='vertical')
        self.wg = Widget()
        self.end = Button(text='Остановить сервер', 
                          pos=(10, 230), 
                          size_hint=(None, None), 
                          size=(200, 100),
                          on_press=self.on_stop,
                          on_release=self.clear)
        self.start = Button(text='Запустить сервер', 
                          pos=(10, 120), 
                          size_hint=(None, None), 
                          size=(150, 100),
                          on_press=self.start_server)     
        self.exit_button = Button(text='Выход',
                          pos=(10, 10), 
                          size_hint=(None, None), 
                          size=(100, 100),
                          on_press=self.exit_press,
                          on_release=self.exit_release)             
                
        layout.add_widget(self.label)
        layout.add_widget(self.log_label)
        self.wg.add_widget(self.end)
        self.wg.add_widget(self.start)
        self.wg.add_widget(self.exit_button)
        layout.add_widget(self.wg)
        self.start_server()
        return layout
   
    def start_server(self, instance=None):
        self.for_log("Запуск сервера в отдельном процессе...")
        self.server_process = Process(target=run_server, daemon=True)
        self.server_process.start()
        if instance:
            with self.wg.canvas.before:
                Color(1, 0, 1, 1)
                BoxShadow(
                    pos=instance.pos,
                    size=instance.size,
                    blur_radius=40)

    def on_stop(self, instance=None):
        if hasattr(self, 'server_process'):
            self.for_log("Попытка остановить серверный процесс...")
            self.server_process.terminate()
            self.server_process.join()
            self.for_log("Серверный процесс завершён.")
        else:
            self.for_log("Серверный процесс не был запущен.")
        if instance:
            with self.wg.canvas.before:
                Color(1, 0, 1, 1)
                BoxShadow(
                    pos=instance.pos,
                    size=instance.size,
                    blur_radius=40)
                
    def clear(self, instance):
        self.wg.canvas.before.clear()


    def exit_press(self, instance):
        if instance:
            with self.wg.canvas.before:
                Color(1, 0, 1, 1)
                BoxShadow(
                    pos=instance.pos,
                    size=instance.size,
                    blur_radius=40)
                
    def exit_release(self, instance=None):
        App.get_running_app().stop()

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
    
# Отдельная функция для запуска сервера
def run_server():
    uvicorn.run(app, host='192.168.1.33', port=8066)


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    MainApp().run()
    # uvicorn.run('main:app', host='192.168.1.33', port=8066, reload=True)
    # uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
    # uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)