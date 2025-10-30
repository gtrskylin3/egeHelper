from fastapi import Depends, FastAPI
from app.models import User
from uvicorn import run
from app.routes import auth_router

app = FastAPI(
    title="EGE-Trainer API"
)

app.include_router(
    auth_router,
    tags=['auth']
)

if __name__ == '__main__':
    run('main:app', reload=True)