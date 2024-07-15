from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import scoped_session
from sqlalchemy.sql import func

from app.infrastructure.postgres.models import SelfPracticeSession, Session


class SessionQueries:
    def __init__(self, db_session: scoped_session) -> None:
        self.__db_session: scoped_session = db_session

    async def create_session(self, session: Session) -> Session:
        self.__db_session.add(session)
        await self.__db_session.flush()
        await self.__db_session.refresh(session)

        return session

    async def create_self_practice_session(
        self, self_practice_session: SelfPracticeSession
    ) -> SelfPracticeSession:
        self.__db_session.add(self_practice_session)
        await self.__db_session.flush()
        await self.__db_session.refresh(self_practice_session)

        return self_practice_session

    async def get_session_by_id(self, id: int) -> Session:
        stmt = select(Session).filter_by(id=id)
        result = await self.__db_session.execute(stmt)
        return result.scalars().first()
