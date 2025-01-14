import io
from datetime import datetime, timezone, timedelta
import jwt
from PIL import Image
from fastapi import UploadFile, HTTPException
import os

from settings import settings_app



def optimaze_image(image_data: bytes) -> bytes:
    with Image.open(io.BytesIO(image_data)) as img:
        img.thumbnail((1024, 1024))
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format=img.format)
        return img_byte_array.getvalue()


def create_token(data: dict):
    data.update({
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings_app.ACCESS_TOKEN_EXPIRE_MIN)
    })
    encoded_jwt = jwt.encode(data, settings_app.SECRET_KEY, algorithm=settings_app.ALGORITHM)
    return encoded_jwt


def decode_token(token):
    try:
        payload = jwt.decode(token, settings_app.SECRET_KEY, algorithms=[settings_app.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as e:
        print(f"Token has expired: {e}")
        return False
    except jwt.PyJWTError as e:
        print(f"Error: token not decode: {e}")
        return False
