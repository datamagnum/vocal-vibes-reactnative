import select
from functools import wraps
from typing import Any, Callable, Coroutine, Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    decode_refresh_token,
)
from app.domain.group.service import GroupService
from app.domain.user.schema import User
from app.exceptions.exceptions_http import GenericNotFoundError, Unauthorized_401
from app.exceptions.exceptions_internal import EntityNotFound, Unauthorized
from app.infrastructure.postgres.models import Group, GroupUsers
from app.infrastructure.postgres.queries.user import UserQueries
from app.infrastructure.postgres.session import aget_session
from app.routes.servicesfac import get_group_service

get_bearer_token = HTTPBearer(auto_error=False)
known_tokens = set([settings.AUTHORIZED_API_KEY])
token_validation_cache = {}


class UnauthorizedMessage(BaseModel):
    detail: str = "Bearer token missing or unknown"


async def validate_api_key(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> str:
    if not auth:
        raise Unauthorized_401(
            ex=Unauthorized(
                message="Auth token not present in authorization header",
                readable_message="Auth token not present in authorization header",
            )
        )

    if auth.credentials not in known_tokens:
        logger.warning("Auth token provided is invalid")
        raise Unauthorized_401(
            ex=Unauthorized(
                message="Invalid Auth token provided",
                readable_message="Invalid Auth token provided",
            )
        )


async def validate_access_token(
    db_session: AsyncSession = Depends(aget_session),
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> User:
    if not auth:
        raise Unauthorized_401(
            ex=Unauthorized(
                message="Bearer token not present in authorization header",
                readable_message="Bearer token not present in authorization header",
            )
        )
    try:
        decoded_data = decode_access_token(access_token=auth.credentials)
    except Exception:
        raise Unauthorized_401(
            ex=Unauthorized(
                message="Invalid Token",
                readable_message="Invalid Token",
            )
        )

    user_queries: UserQueries = UserQueries(db_session=db_session)

    user_orm = await user_queries.get_by_email(email=decoded_data["sub"])

    return User.create_from_orm(orm_obj=user_orm)


async def renew_access_token(
    request: Request,
    db_session: AsyncSession = Depends(aget_session),
) -> str:
    payload = await request.json()
    refresh_token = payload.get("refresh_token")

    if not refresh_token:
        raise Unauthorized_401(
            ex=Unauthorized(
                message="No Refresh Token Found",
                readable_message="No Refresh Token Found",
            )
        )
    try:
        decoded_data = decode_refresh_token(access_token=refresh_token)
    except Exception:
        raise Unauthorized_401(
            ex=Unauthorized(
                message="Invalid Token",
                readable_message="Invalid Token",
            )
        )

    user_queries: UserQueries = UserQueries(db_session=db_session)

    user_orm = await user_queries.get_by_email(email=decoded_data["sub"])
    return create_access_token(subject=user_orm.email)


async def verify_group_owner(
    group_id: str,
    user: User = Depends(validate_access_token),
    group_service: GroupService = Depends(get_group_service),
) -> Group:
    group = await group_service.get_group(group_id)

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if group.created_by != user.id:
        raise HTTPException(
            status_code=403, detail="User is not the owner of this group"
        )

    return group
