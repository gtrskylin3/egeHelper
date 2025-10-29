from fastapi import Depends
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from app.config import jwt_settings

SECRET_PRIVATE_KEY = jwt_settings.PRIVATE_KEY.read_text('utf-8')
SECRET_PUBLIC_KEY = jwt_settings.PUBLIC_KEY.read_text('utf-8')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=SECRET_PRIVATE_KEY, 
        lifetime_seconds=3600, # 1 час
        algorithm=jwt_settings.ALGORITHM,
        public_key=SECRET_PUBLIC_KEY
    )

cookie_transport = CookieTransport(cookie_name="ege_trainer", cookie_max_age=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
