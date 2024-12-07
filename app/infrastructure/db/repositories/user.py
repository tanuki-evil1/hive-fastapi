from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.user import UserSchema
from app.infrastructure.db.models.user import User
from app.infrastructure.db.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Репозиторий для пользователей."""

    model = User
    schema = UserSchema

    def __init__(self, session: AsyncSession):
        super().__init__(session, model=self.model, schema=self.schema)
