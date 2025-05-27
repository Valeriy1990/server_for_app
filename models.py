from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    login: str = ''
    password: str = ''
 
class Climate(BaseModel):
    humidity: int | float
    temperature: int | float
    room: int
    login: str
    creation_date: datetime

    