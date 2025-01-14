from fastapi import FastAPI

import uvicorn
from app.routes import users_route, pictures_route, auth_route

app = FastAPI(docs_url="/",
              title="Santar4 API",
              description="///",
              )

app.include_router(users_route, prefix="/user", tags=["users"])
app.include_router(auth_route, prefix="/auth", tags=["auth"])
app.include_router(pictures_route, prefix="/pictures", tags=["pictures"])

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
