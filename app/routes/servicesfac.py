from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.domain.auth.service import AuthService
from app.domain.group.service import GroupService
from app.domain.session.service import SessionService
from app.domain.sso.service import SSOService
from app.domain.topic.service import TopicService
from app.domain.user.service import UserService
from app.infrastructure.postgres.queries.user import UserQueries
from app.infrastructure.postgres.session import aget_session


async def get_user_service(
    db_session: AsyncSession = Depends(aget_session),
) -> UserService:
    user_queries = UserQueries(db_session)
    return UserService(user_queries)


async def get_sso_service() -> SSOService:
    return SSOService()


async def get_auth_service(
    db_session: AsyncSession = Depends(aget_session),
    sso_service: SSOService = Depends(get_sso_service),
) -> AuthService:
    return AuthService(db_session=db_session, sso_service=sso_service)


async def get_topic_service(
    db_session: AsyncSession = Depends(aget_session),
) -> TopicService:
    return TopicService(db_session=db_session)


async def get_session_service(
    db_session: AsyncSession = Depends(aget_session),
) -> SessionService:
    return SessionService(db_session=db_session)


async def get_group_service(
    db_session: AsyncSession = Depends(aget_session),
) -> GroupService:
    return GroupService(db_session=db_session)
