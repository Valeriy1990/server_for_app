from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout


import uvicorn


# logger = logging.getLogger(__name__)

class MainApp(MDApp):

    def build(self):
        exit_button = MDFloatingActionButton(icon="exit-run",
                                    md_bg_color = (0, 1, 0.7, 0.7),
                                    icon_color=(1, 1, 1, 1),
                                    on_press=self.on_stop,
                                    # on_press=self.on_start,
                                    pos_hint={"center_x": 0.85, "center_y": 0.08})
        
        server_button = MDFloatingActionButton(icon="exit-run",
                                    md_bg_color = (0, 1, 0.7, 0.7),
                                    icon_color=(1, 1, 1, 1),
                                    on_press=self.server,
                                    # on_press=self.on_start,
                                    pos_hint={"center_x": 0.5, "center_y": 0.5})
        
        '''Создание пустого макета, не привязанного к экрану'''
        main_layout = MDBoxLayout(orientation="vertical")   
        
        main_layout.add_widget(exit_button)
        main_layout.add_widget(server_button)

        return main_layout
    
    def on_stop(self, instance):
        '''Завершить приложение'''
        # logger.info('Успешный выход из программы. Ты супер!!')
        # self.profile.disable()
        # self.profile.dump_stats('my_exe_client/myapp.profile')
        # self.save()
        App.get_running_app().stop()

    # def server(self, instance):
    #     uvicorn.run('server:app', host='192.168.1.33', port=8066)

if __name__ == "__main__":
    MainApp().run()