from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.domain.group.schema import ListUserGroupsResponseSchema
from app.domain.group.service import GroupService
from app.domain.user.schema import ListUserResponseSchema, User
from app.domain.user.service import UserService
from app.routes.deps.security import validate_access_token
from app.routes.servicesfac import get_group_service, get_user_service

router = APIRouter()


@router.get("/whoami")
async def whoami(user: User = Depends(validate_access_token)) -> User:
    return user


@router.get("/users", response_model=ListUserResponseSchema)
async def list_users(
    user_service: UserService = Depends(get_user_service),
    _: User = Depends(validate_access_token),
) -> ListUserResponseSchema:
    return await user_service.get_users()


@router.get("/group", response_model=ListUserGroupsResponseSchema)
async def list_user_groups(
    group_service: GroupService = Depends(get_group_service),
    user: User = Depends(validate_access_token),
) -> ListUserGroupsResponseSchema:
    return await group_service.list_user_groups(user_id=user.id)
