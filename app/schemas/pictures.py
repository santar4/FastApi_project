from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class PictureSchema(BaseModel):
    name: str = Field(..., min_length=2,
                          description="Назва має мати, що найменше, а ніж 2 символи")

    description: str = Field(..., max_length=200,
                          description="Опис, немає перевищувати 200 символів")

    date: datetime = Field(datetime.now())

    tag: str = Field(..., min_length=2,
                          description="Мінімум 82 символів, включає велику, маленьку літеру, цифру і спеціальний символ")

