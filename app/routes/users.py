
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import generate_password_hash
from app.models import User
from app.schemas import InputUserData, UserSchema
from settings import get_session

route = APIRouter()


@route.post("/")
async def registration(data_user: InputUserData,
                       session: AsyncSession = Depends(get_session)):
    stmt = select(User).filter_by(email=data_user.email)
    user = await session.scalar(stmt)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is exists")

    user_dict = data_user.model_dump()
    user_dict["password_hash"] = generate_password_hash(user_dict["password"])
    del user_dict["password_repeat"]
    del user_dict["password"]

    new_user = User(**user_dict)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return UserSchema.model_validate(new_user)