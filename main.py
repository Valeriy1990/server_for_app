# uvicorn server_for_app.main:app --reload 
# http://localhost:8000
# http://localhost:8000/docs

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import BoxShadow, Color
from kivy.config import Config
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout


Config.set("graphics", "width", "400")
Config.set("graphics", "height", "700")
Config.set("graphics", "resizable", "0")

# from kivy.uix.textinput import TextInput
from datetime import datetime
from loggers import logger
import matplotlib.pyplot as plt
import uvicorn
import logging
import sys
from environs import Env
from multiprocessing import Process
import pandas as pd
from docxtpl import DocxTemplate
from my_app import app
from models import RoundedButton
from logging_settings import logging_config
import logging.config

env = Env()  # Создаем экземпляр класса Env
env.read_env('inter.env') # Методом read_env() читаем файл .env и загружаем из него переменные в окружение
                          
ip = env('ip')  # Получаем и сохраняем значение переменной окружения в переменную
port = env('PORT')
user = eval(env('user'))

# logger = logging.getLogger(__name__)
# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setFormatter(logging.Formatter('--> [%(levelname)-8s] - [Line %(lineno)d : def %(funcName)s : %(filename)s] - %(message)s'))
# stdout_handler.setFormatter(logging.Formatter('--> %(message)s'))
# logger.addHandler(stdout_handler)

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)
logging.getLogger('matplotlib').setLevel(logging.WARNING)

class MainApp(App):
    buttons = tuple(num for num in range(536,550) if num != 547)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_text = ""
        try:
            # self.data = pd.read_csv(r'C:\Users\vbekr\OneDrive\Рабочий стол\Python\server_for_app\data.csv', delimiter=',')
            self.data = pd.read_csv('data.csv', delimiter=',')
        except Exception as e:
            logger.info(f'{e}')
            self.data = None

    def for_log(self, message):
        # self.log_text += message + "\n"
        self.log_text = message + "\n"
        if hasattr(self, 'log_label'):
            self.log_label.text = self.log_text 

    def build(self):
        self.label = Label(text="")  # Надо как-то убрать
        self.log_label = Label(text="", size_hint_y=None)
        layout = BoxLayout(orientation='vertical')
        self.wg = Widget()
        
        self.end = RoundedButton(text='Остановить сервер', 
                          pos=(10, 230), 
                          size_hint=(None, None), 
                          size=(200, 100),
                          on_press=self.on_stop,
                          on_release=self.clear)
        self.start = RoundedButton(text='Запустить сервер', 
                          pos=(10, 120), 
                          size_hint=(None, None), 
                          size=(150, 100),
                          on_press=self.start_server,
                          on_release=self.clear)     
        self.exit_button = RoundedButton(text='Выход',
                          pos=(10, 10), 
                          size_hint=(None, None), 
                          size=(100, 100),
                          on_press=self.exit_press,
                          on_release=self.exit_release)             
        self.docx_button = RoundedButton(text='Получить данные',
                          pos=(120, 10), 
                          size_hint=(None, None), 
                          size=(270, 100),
                          on_press=self.docx_press,
                          on_release=self.clear)  
        
        tb = TabbedPanel(do_default_tab=False, tab_pos="top_left")
        tbi = TabbedPanelItem(text="Линия")
        tbi_1 = TabbedPanelItem(text="...")
        tbi_2 = TabbedPanelItem(text="...")
        bl = GridLayout(rows=3)

        for num in self.buttons:
            button_room = Button(size_hint=(0.2, 0.1), 
                                 text=str(num),
                                 on_press=self.gr_press,
                                 on_release=self.clear)

            button_room.name = str(num)
            bl.add_widget(button_room)
            tbi.add_widget(bl) 
        
        tb.add_widget(tbi)
        tb.add_widget(tbi_1)
        tb.add_widget(tbi_2)
        layout.add_widget(tb)
        layout.add_widget(self.log_label)               
        layout.add_widget(self.label)
        self.wg.add_widget(self.end)
        self.wg.add_widget(self.start)
        self.wg.add_widget(self.exit_button)
        self.wg.add_widget(self.docx_button)
        layout.add_widget(self.wg)

        return layout
   
    def start_server(self, instance=None):
        self.for_log("Запуск сервера")
        logger.info("Запуск сервера в отдельном процессе...")
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
            logger.info("Серверный процесс завершён.")
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

    def docx_press(self, instance):
        if instance:
            with self.wg.canvas.before:
                Color(1, 0, 1, 1)
                BoxShadow(
                    pos=instance.pos,
                    size=instance.size,
                    blur_radius=40)

        context = {'date' : datetime.now().date()}

        self.for_log("Запись в doc файл")
        logger.info(f'Запись в doc файл')
        # doc = DocxTemplate(r'C:\Users\vbekr\OneDrive\Рабочий стол\Python\server_for_app\Шаблон.docx')
        doc = DocxTemplate('Шаблон.docx')
            
        for num in self.buttons:
            if num in tuple(self.data['room']):
                # res = self.data.query(f'room == {num}')
                res = self.data.loc[self.data.room == num]
                context[f'room_{num}'] = num

                context[f'humidity_{num}_1'] = res.iloc[-1].humidity
                context[f'time_{num}_1'] = datetime.fromisoformat(res.iloc[-1].date).strftime('%H:%M:%S')
                context[f'temperature_{num}_1'] = res.iloc[-1].temperature

                context[f'humidity_{num}_2'] = res.iloc[-2].humidity
                context[f'time_{num}_2'] = datetime.fromisoformat(res.iloc[-2].date).strftime('%H:%M:%S')
                context[f'temperature_{num}_2'] = res.iloc[-2].temperature

        try:
            doc.render(context)
            # doc.save(r'C:\Users\vbekr\OneDrive\Рабочий стол\Python\server_for_app\Отчёт.docx')
            doc.save('Отчёт.docx')
        except Exception as e:
            logger.info(f'{e}')

    def gr_press(self, instance):
        if instance:
            with self.wg.canvas.before:
                Color(1, 0, 1, 1)
                BoxShadow(
                    pos=instance.pos,
                    size=instance.size,
                    blur_radius=40)

        if instance.name in tuple(map(str, self.data['room'])):
            data = self.data.query(f'room == {instance.name}')

            # Данные для графика:  
            x = tuple(str(datetime.fromisoformat(dt).date()) for dt in data['date'])
            y1 = data['humidity'] 
            y2 = data['temperature']
            # Создание линейного графика:  
            plt.plot(x, y1)  
            plt.plot(x, y2) 
            plt.ylabel('Влажность / Температура ')
            plt.xlabel('Дата')
            plt.legend(['Влажность','Температура'], loc='upper left')
            # Отображение графика:  
            plt.show()  

# Отдельная функция для запуска сервера
def run_server():
    uvicorn.run(app, host=str(ip), port=int(port), log_level="warning")
    # uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    MainApp().run()
