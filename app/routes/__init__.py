from .auth import router as auth_router
from .subjects import router as subjects_router
from .sessions import router as sessions_router
# from . import router
# from . import router
# from . import router

__all__ = [
    'auth_router',
    'subjects_router',
    'sessions_router'
]