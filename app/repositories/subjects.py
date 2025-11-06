from app.models.subjects import Subject
from app.schemas.subjects import SubjectCreate, SubjectUpdate
from .base import BaseRepository


class SubjectRepository(BaseRepository[Subject, SubjectCreate, SubjectUpdate]):
    pass

subject_repository = SubjectRepository(Subject)
