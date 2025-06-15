from pydantic import BaseModel
from datetime import datetime
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

class User(BaseModel):
    """Для аутентификации"""
    login: str = ''
    password: str = ''
 
class Climate(BaseModel):
    """Формат входящих климатических параметров"""
    humidity: int | float
    temperature: int | float
    room: int
    login: str
    creation_date: datetime

class RoundedButton(Button):
    """Кастомная кнопка"""
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0) # Убираем стандартный фон
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0.6, 1, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[(20, 20)])
        with self.canvas.after:
            Color(0, 0, 0, 0.3)
            self.shadow = RoundedRectangle(size=(self.width + 10, self.height + 10), pos=(self.x - 5, self.y - 5), radius=[(20, 20)])

    def update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.x - 5, self.y - 5)
        self.shadow.size = (self.width + 10, self.height + 10)
    