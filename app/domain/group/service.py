from typing import List, Optional

from sqlalchemy.orm import scoped_session

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
from app.domain.user.schema import User
from app.infrastructure.postgres.models import Group as GroupOrm
from app.infrastructure.postgres.models import GroupUsers as GroupUsersORM
from app.infrastructure.postgres.queries.group import GroupQueries


class GroupService:
    def __init__(self, db_session: scoped_session) -> None:
        self.__group_queries: GroupQueries = GroupQueries(db_session=db_session)

    async def create_group(
        self, payload: CreateGroupRequestSchema, user: User
    ) -> Group:
        payload.created_by = user.id
        group_orm = await self.__group_queries.create_group(payload.orm_obj)

        group_user_orm = GroupUsersORM(
            group_id=group_orm.id,
            user_id=user.id,
        )
        await self.__group_queries.add_user_to_group(
            group_id=group_user_orm.group_id, user_id=group_user_orm.user_id
        )
        return Group.create_from_orm(group_orm)

    async def add_user_to_group(self, user_id: int, group_id: str):
        group_user_orm = await self.__group_queries.add_user_to_group(
            group_id=group_id, user_id=user_id
        )

        if group_user_orm:
            return {"message": "User has been added from the group"}

    async def remove_user_from_group(self, user_id: int, group_id: str) -> None:
        await self.__group_queries.remove_user_from_group(
            group_id=group_id, user_id=user_id
        )

    async def list_user_groups(self, user_id: int) -> ListUserGroupsResponseSchema:
        groups_orm = await self.__group_queries.list_user_groups(user_id)
        groups = [Group.create_from_orm(group) for group in groups_orm]

        return ListUserGroupsResponseSchema(groups=groups)

    async def get_group(self, group_id: str) -> Optional[Group]:
        group_orm = await self.__group_queries.get_group_by_id(group_id)
        if group_orm:
            return Group.create_from_orm(group_orm)
        else:
            return None

    async def get_users_in_group(
        self, group_id: str
    ) -> ListUsersInGroupsResponseSchema:
        users_orms = await self.__group_queries.get_users_in_group(group_id)
        users = [User.create_from_orm(orm_obj) for orm_obj in users_orms]
        return ListUsersInGroupsResponseSchema(users=users)
