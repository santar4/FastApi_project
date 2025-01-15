import os

import uvicorn
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException, status

route = APIRouter()

Max_file_size = 20 * 1024 * 1024
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


@route.post("/image/upload")
async def upload_image(background_tasks: BackgroundTasks,
                       files: list[UploadFile] = File(..., description="upload your image")):
    return {"detail": "Фотографію завантажено"}


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
