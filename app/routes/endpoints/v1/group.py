from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.domain.group.schema import (
    AddUserToGroupRequestSchema,
    CreateGroupRequestSchema,
    GetGroupRequestSchema,
    Group,
    GroupUser,
    ListUserGroupsResponseSchema,
    ListUsersInGroupsResponseSchema,
    RemoveUserFromGroupRequestSchema,
)
from app.domain.group.service import GroupService
from app.domain.user.schema import User
from app.exceptions.exceptions_http import DuplicateEntityError, Unauthorized_401
from app.exceptions.exceptions_internal import (
    DuplicateEntity,
    EntityNotFound,
    Unauthorized,
)
from app.routes.deps.security import validate_access_token, verify_group_owner
from app.routes.servicesfac import get_group_service

router = APIRouter()


@router.post("", response_model=Group)
async def create_group(
    payload: CreateGroupRequestSchema,
    user: User = Depends(validate_access_token),
    group_service: GroupService = Depends(get_group_service),
) -> Group:
    return await group_service.create_group(payload=payload, user=user)


@router.post("/{group_id}/user/{user_id}")
async def add_user_to_group(
    group_id: str,
    user_id: int,
    group_service: GroupService = Depends(get_group_service),
    _=Depends(verify_group_owner),
):
    await group_service.add_user_to_group(user_id=user_id, group_id=group_id)
    return {"message": "User has been Added from the group"}


@router.delete("/{group_id}/user/{user_id}", status_code=status.HTTP_200_OK)
async def remove_user_from_group(
    group_id: str,
    user_id: int,
    group_service: GroupService = Depends(get_group_service),
    _=Depends(verify_group_owner),
):
    await group_service.remove_user_from_group(user_id=user_id, group_id=group_id)
    return {"message": "User has been removed from the group"}


@router.get("/{group_id}", response_model=Group)
async def get_group(
    group_id: str,
    user: User = Depends(validate_access_token),
    group_service: GroupService = Depends(get_group_service),
) -> Group:
    payload = GetGroupRequestSchema(group_id=group_id)
    group = await group_service.get_group(payload=payload)
    if group:
        return group
    else:
        raise EntityNotFound("Group not found")


@router.get("/{group_id}/users", response_model=ListUsersInGroupsResponseSchema)
async def get_users_in_group(
    group_id: str,
    group_service: GroupService = Depends(get_group_service),
    _=Depends(verify_group_owner),
) -> ListUsersInGroupsResponseSchema:
    return await group_service.get_users_in_group(group_id=group_id)
