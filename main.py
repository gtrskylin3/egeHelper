from fastapi import Depends, FastAPI

from app.core.auth import auth_backend
from app.core.users import get_user_manager
from app.database.db import create_db_and_tables
from app.schemas.users import UserCreate, UserRead
from app.models import User
from uvicorn import run
from fastapi_users import FastAPIUsers

app = FastAPI(
    title="EGE-Trainer API"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Роутер для /login, /logout
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Роутер для /register
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Защищенный роут для проверки текущего пользователя
current_active_user = fastapi_users.current_user(active=True)

@app.get("/users/me", tags=["users"], response_model=UserRead)
async def read_users_me(user: User = Depends(current_active_user)):
    return user


if __name__ == '__main__':
    run('main:app', reload=True)