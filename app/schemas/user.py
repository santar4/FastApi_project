import re
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    bio: Optional[str] = Field(None)
    date: datetime = Field(datetime.now())
