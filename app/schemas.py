from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Схема для создания нового изображения
class ImageCreate(BaseModel):
    name: str
    file_path: str
    resolution: str
    size: int

# Схема для отображения информации об изображении
class ImageOut(BaseModel):
    id: int
    name: str
    file_path: str
    upload_date: datetime
    resolution: str
    size: int

    class Config:
        orm_mode = True  # Позволяет Pydantic работать с ORM-объектами, такими как SQLAlchemy

# Схема для обновления информации об изображении
class ImageUpdate(BaseModel):
    name: Optional[str] = None
    file_path: Optional[str] = None
    resolution: Optional[str] = None
    size: Optional[int] = None

# Схема для создания нового пользователя
class UserCreate(BaseModel):
    username: str
    password: str

# Схема для выдачи токена
class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
