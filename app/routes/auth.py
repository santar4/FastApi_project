from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy import select

from settings import *
from app.models import User
from settings import settings_app as s, async_session
from app.tools import decode_token, create_token

route = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@route.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(),
                         session: AsyncSession = Depends(async_session)):
    async with session.begin():
        user = await session.execute(select(User).where(User.username == form_data.username))
        user = user.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Невірне ім'я користувача або пароль")

        try:
            user_data_from_token = decode_token(user.password_hash)

            if not user_data_from_token or user_data_from_token.get("password") != form_data.password:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Невірне ім'я користувача або пароль",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Помилка при перевірці пароля: " + str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_token({"username": user.username, "id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_data = decode_token(token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний токен",
            headers={"Authorization": "Bearer"},
        )
    return user_data
