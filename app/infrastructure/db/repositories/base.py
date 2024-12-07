from typing import Any, Optional, Type

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """Репозиторий, реализующий CRUD-операции с базой данных через SQLAlchemy.

    Позволяет взаимодействовать с моделью базы данных с использованием асинхронных сессий.
    """

    def __init__(
            self,
            session: AsyncSession,
            model: Any,
            schema: Optional[Type[BaseModel]] = None,
    ):
        """
        Инициализация репозитория.

        :param session: Асинхронная сессия SQLAlchemy.
        :param model: Модель базы данных для работы с таблицей.
        :param schema: Pydantic-схема для сериализации и десериализации данных.
        """
        self.session = session
        self.model = model
        self.schema = schema
        self.name = self.model.__name__

    async def find_one(self, filter_by: dict[str, Any]):
        """
        Ищет одну запись в базе данных по фильтру.

        :param filter_by: Фильтр для поиска.
        :return: Экземпляр модели или None, если запись не найдена.
        """
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        return self.schema.model_validate(instance, from_attributes=True) if instance else None
