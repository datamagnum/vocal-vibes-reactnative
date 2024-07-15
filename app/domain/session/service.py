from typing import List

from sqlalchemy.orm import scoped_session

from app.domain.session.schema import (
    CreateSelfPracticeSessionRequestSchema,
    CreateSessionRequestSchema,
    SelfPracticeSession,
    Session,
)
from app.domain.user.schema import User
from app.infrastructure.postgres.models import (
    SelfPracticeSession as SelfPracticeSessionOrm,
)
from app.infrastructure.postgres.models import Session as SessionOrm
from app.infrastructure.postgres.queries.session import SessionQueries


class SessionService:
    def __init__(self, db_session: scoped_session) -> None:
        self.__session_queries: SessionQueries = SessionQueries(db_session=db_session)

    async def create_session(
        self, payload: CreateSessionRequestSchema, user: User
    ) -> Session:
        payload.created_by = user.id

        session_orm = await self.__session_queries.create_session(payload.orm_obj)

        return Session.create_from_orm(session_orm)

    async def create_self_practice_session(
        self, payload: CreateSelfPracticeSessionRequestSchema
    ) -> SelfPracticeSession:

        session_orm = await self.__session_queries.create_self_practice_session(
            payload.orm_obj
        )

        return SelfPracticeSession.create_from_orm(session_orm)
