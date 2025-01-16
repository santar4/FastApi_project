import os
from typing import List

import uvicorn
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException, status, Depends, Form
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Picture, User, Tag
from app.routes.auth import get_current_user
from settings import async_session

route = APIRouter()

MAX_FILE_SIZE = 20 * 1024 * 1024
ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/gif", "image/bmp"}


@route.post("/image/upload")
async def upload_image(
        name: str = Form(..., description="Image name"),
        description: str = Form(..., description="Image description"),
        tag: str = Form(..., description="Tag (theme) of the image"),
        file: UploadFile = File(..., description="Upload your image"),
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_session)
):
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Не підтримуємий тип картинки: {file.filename}")

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"Не підтримуємий тип картинки: {file.filename}")

    existing_tag = await session.execute(select(Tag).where(Tag.name == tag))
    existing_tag = existing_tag.scalars().first()

    if not existing_tag:
        existing_tag = Tag(name=tag)
        session.add(existing_tag)

    new_picture = Picture(
        image=content,
        name=name,
        description=description,
        tag=tag,
        author_id=current_user.id,
        tags=[existing_tag]
    )

    session.add(new_picture)
    await session.commit()
    return {"detail": "Image uploaded successfully", "image_id": new_picture.id}


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
