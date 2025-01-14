import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_sso import GoogleSSO
from fastapi.requests import Request
from sqlalchemy import select
from sqlalchemy.orm import session, selectinload
from settings import *
from app.models import User
from settings import settings_app as s, async_session
from app.tools import decode_token, create_token

route = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# async def get_google_sso() -> GoogleSSO:
#     async with GoogleSSO(s.GOOGLE_CLIENT_ID,
#                          s.GOOGLE_CLIENT_SECRET,
#                          redirect_uri=f"http://{s.HOST}:{s.PORT}/auth/google/callback") as provider:
#         return provider
#
#
# @route.get("/google/login")
# async def google_login(google_sso: GoogleSSO = Depends(get_google_sso)):
#     return await google_sso.get_login_redirect()
#
#
# @route.get("/google/callback")
# async def google_callback(request: Request, google_sso: GoogleSSO = Depends(get_google_sso),
#                           session: AsyncSession = Depends(get_session)):
#     user_data = await google_sso.verify_and_process(request)
#
#     user = await session.execute(
#         select(User).where(User.google_id == user_data["id"]).options(selectinload(User))
#     )
#     user = user.scalar_one_or_none()
#
#     if not user:
#         user = User(
#             username=user_data["name"],
#             email=user_data["email"],
#             google_id=user_data["id"],
#             password_hash=None,
#         )
#         session.add(user)
#         await session.commit()
#
#     return {"id": user.id, "username": user.username, "email": user.email}


# @route.post("/token")
# async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(),
#                          session: AsyncSession = Depends(async_session)):
#     async with session.begin():
#         user = await session.execute(select(User).where(User.username == form_data.username))
#         user = user.scalar_one_or_none()
#
#         if not user:
#             raise HTTPException(status_code=400, detail="Невірне ім'я користувача або пароль")
#
#         try:
#             decoded_password = jwt.decode(user.password_hash, s.SECRET_KEY, algorithms=[s.ALGORITHM])["password"]
#         except Exception:
#             raise HTTPException(status_code=400, detail="Помилка при перевірці пароля")
#
#         if decoded_password != form_data.password:
#             raise HTTPException(status_code=400, detail="Невірне ім'я користувача або пароль")
#
#         access_token = create_token(data={"username": user.username, "id": user.id})
#         return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_data = decode_token(token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний токен",
            headers={"Authorization": "Bearer"},
        )
    return user_data
