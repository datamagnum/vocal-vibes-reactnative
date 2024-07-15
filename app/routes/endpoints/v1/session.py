from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.domain.session.schema import (
    CreateSelfPracticeSessionRequestSchema,
    CreateSessionRequestSchema,
    SelfPracticeSession,
    Session,
)
from app.domain.session.service import SessionService
from app.domain.user.schema import User
from app.exceptions.exceptions_http import DuplicateEntityError, Unauthorized_401
from app.exceptions.exceptions_internal import (
    DuplicateEntity,
    EntityNotFound,
    Unauthorized,
)
from app.routes.deps.security import validate_access_token
from app.routes.servicesfac import get_session_service

router = APIRouter()


@router.post("", response_model=Session)
async def create_session(
    payload: CreateSessionRequestSchema,
    user: User = Depends(validate_access_token),
    session_service: SessionService = Depends(get_session_service),
) -> Session:
    return await session_service.create_session(payload=payload, user=user)


@router.post("/practice", response_model=SelfPracticeSession)
async def create_self_practice_session(
    payload: CreateSelfPracticeSessionRequestSchema,
    user: User = Depends(validate_access_token),
    session_service: SessionService = Depends(get_session_service),
) -> SelfPracticeSession:
    return await session_service.create_self_practice_session(payload=payload)


# @router.get(
#     "",
# )
# async def get_topics(
#     _: User = Depends(validate_access_token),
#     page: int = Query(1, gt=0),
#     per_page: int = Query(10, gt=0),
#     topic_service: TopicService = Depends(get_topic_service),
# ) -> TopicsResponseSchema:
#     return await topic_service.get_topics(page=page, per_page=per_page)
