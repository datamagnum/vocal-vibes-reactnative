from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import scoped_session
from sqlalchemy.sql import func

from app.infrastructure.postgres.models import Topic


class TopicQueries:
    def __init__(self, db_session: scoped_session) -> None:
        self.__db_session: scoped_session = db_session

    async def create(self, topic: Topic) -> Topic:
        self.__db_session.add(topic)
        await self.__db_session.flush()
        await self.__db_session.refresh(topic)

        return topic

    async def get_by_id(self, id: int) -> Topic:
        stmt = select(Topic).filter_by(id=id)
        result = await self.__db_session.execute(stmt)
        return result.scalars().first()

    async def get_total_topics(self) -> int:
        stmt = select(func.count(Topic.id))
        result = await self.__db_session.execute(stmt)
        total_topics = result.scalar()
        return total_topics

    async def get_paginated_topics(self, page: int, per_page: int) -> List[Topic]:
        stmt = select(Topic).limit(per_page).offset((page - 1) * per_page)
        result = await self.__db_session.execute(stmt)
        return result.scalars().all()
