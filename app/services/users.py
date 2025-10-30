from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Form
from app.auth import utils
from app.models.users import User
from app.repositories.users import user_repository
from app.schemas.users import UserCreate, UserRead, UserScheme


class UserService:
    async def create_user(self, db: AsyncSession, *, user_in: UserCreate) -> UserRead:
        # 1. Проверяем, существует ли пользователь
        existing_user = await user_repository.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        # 2. Готовим данные для сохранения в БД
        create_data = user_in.model_dump()

        # 3. Хешируем пароль и заменяем поле
        hashed_password = utils.hash_password(user_in.password)
        create_data.pop("password")  # Удаляем пароль в открытом виде
        create_data["password_hash"] = hashed_password  # Добавляем хеш

        # 4. Передаем в репозиторий чистые данные
        user = await user_repository.create(db, user_data=create_data)
        return UserRead.model_validate(user)

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> UserRead:
        user = await user_repository.get(db, user_id)
        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found"
            )
        return UserRead.model_validate(user)

    async def get_user_by_email(self, db: AsyncSession, email: str) -> UserRead:
        user = await user_repository.get_by_email(db, email)
        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found"
            )
        return UserRead.model_validate(user)

    async def get_user_by_username(self, db: AsyncSession, username: str) -> UserRead:
        user = await user_repository.get_by_username(db, username)
        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=f"User with email {username} not found",
            )
        return UserRead.model_validate(user)

    async def get_multi_user(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[UserRead]:
        users = await user_repository.get_multi(db, skip=skip, limit=limit)
        if not users:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=f"no have users with id in range {limit - skip}",
            )
        return [UserRead.model_validate(user) for user in users]

    async def validate_user_credentials(
        self, db: AsyncSession, email: str = Form(), password: str = Form()
    ) -> UserScheme:
        """
        Валидирует username и password при логине.

        Args:
            username: Имя пользователя из формы
            password: Пароль из формы

        Returns:
            UserScheme: Аутентифицированный пользователь

        Raises:
            HTTPException: Если credentials неверны или пользователь неактивен
        """
        user = await user_repository.get_by_email(db, email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not utils.validate_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid emailor password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
            )

        return UserScheme.model_validate(user)


user_service = UserService()
