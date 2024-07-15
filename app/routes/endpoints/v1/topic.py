from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.domain.topic.schema import (
    CreateTopicRequestSchema,
    Topic,
    TopicsResponseSchema,
)
from app.domain.topic.service import TopicService
from app.domain.user.schema import User
from app.exceptions.exceptions_http import DuplicateEntityError, Unauthorized_401
from app.exceptions.exceptions_internal import (
    DuplicateEntity,
    EntityNotFound,
    Unauthorized,
)
from app.routes.deps.security import validate_access_token, validate_api_key
from app.routes.servicesfac import get_topic_service

router = APIRouter()


@router.post(
    "",
)
async def create_topic(
    payload: CreateTopicRequestSchema,
    _=Depends(validate_api_key),
    topic_service: TopicService = Depends(get_topic_service),
) -> Topic:
    return await topic_service.create_topic(payload=payload)


@router.get(
    "",
)
async def get_topics(
    _: User = Depends(validate_access_token),
    page: int = Query(1, gt=0),
    per_page: int = Query(10, gt=0),
    topic_service: TopicService = Depends(get_topic_service),
) -> TopicsResponseSchema:
    return await topic_service.get_topics(page=page, per_page=per_page)
