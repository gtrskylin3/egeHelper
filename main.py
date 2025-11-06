from fastapi import Depends, FastAPI
from app.models import User
from uvicorn import run
from app.routes import auth_router, subjects_router, sessions_router, notes_router

app = FastAPI(
    title="EGE-Trainer API"
)

app.include_router(
    auth_router,
    tags=['auth']
)

app.include_router(
    subjects_router,
    tags=['subjects']
)

app.include_router(
    sessions_router,
    tags=['sessions']
)

app.include_router(
    notes_router,
    tags=['notes']
)

if __name__ == '__main__':
    run('main:app', reload=True)