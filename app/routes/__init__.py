from .auth import router as auth_router
from .subjects import router as subjects_router
from .sessions import router as sessions_router
from .notes import router as notes_router
from .tasks import router as tasks_router
# from . import router
# from . import router

__all__ = [
    'auth_router',
    'subjects_router',
    'sessions_router',
    'notes_router',
    'tasks_router'
]