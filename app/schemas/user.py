import re
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator, ConfigDict


class InputUserData(BaseModel):
    username: str = Field(..., min_length=2,
                          description="Лише літери, мінімум 2 символи")
    email: EmailStr

    password: str = Field(..., min_length=8,
                          description="Мінімум 8 символів, включає велику, маленьку літеру, цифру і спеціальний символ")

    password_repeat: str = Field(min_length=8)

    create_date: datetime = Field(datetime.now())

    @model_validator(mode="after")
    @classmethod
    def valid_pass(cls, data: Any):
        if data.password != data.password_repeat:
            raise ValueError("passwords not match")
        return data

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError("Пароль повинен містити хоча б одну велику літеру")
        if not re.search(r'[a-z]', value):
            raise ValueError("Пароль повинен містити хоча б одну маленьку літеру")
        if not re.search(r'\d', value):
            raise ValueError("Пароль повинен містити хоча б одну цифру")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("Пароль повинен містити хоча б один спеціальний символ")
        return value


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    bio: Optional[str] = Field(None)
    date: datetime = Field(datetime.now())
