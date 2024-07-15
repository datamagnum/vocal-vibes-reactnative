from typing import List, Optional, Tuple

from sqlalchemy.future import select
from sqlalchemy.orm import scoped_session

from app.infrastructure.postgres.models import Group as GroupORM
from app.infrastructure.postgres.models import GroupUsers as GroupUsersORM
from app.infrastructure.postgres.models import User as UserORM


class GroupQueries:
    def __init__(self, db_session: scoped_session) -> None:
        self.__db_session: scoped_session = db_session

    async def create_group(self, group: GroupORM) -> GroupORM:
        self.__db_session.add(group)
        await self.__db_session.flush()
        await self.__db_session.refresh(group)
        return group

    async def get_group_by_id(self, group_id: str) -> Optional[GroupORM]:
        stmt = select(GroupORM).filter_by(id=group_id)
        result = await self.__db_session.execute(stmt)
        return result.scalars().first()

    async def add_user_to_group(
        self,
        group_id: int,
        user_id: int,
    ) -> GroupUsersORM:
        group_user = GroupUsersORM(
            group_id=group_id,
            user_id=user_id,
        )
        self.__db_session.add(group_user)
        await self.__db_session.flush()
        await self.__db_session.refresh(group_user)
        return group_user

    async def remove_user_from_group(self, group_id: int, user_id: int) -> None:
        stmt = select(GroupUsersORM).filter_by(group_id=group_id, user_id=user_id)
        result = await self.__db_session.execute(stmt)
        group_user = result.scalars().first()
        if group_user:
            await self.__db_session.delete(group_user)
            await self.__db_session.commit()

    async def list_user_groups(self, user_id: int) -> List[GroupORM]:
        stmt = (
            select(GroupORM)
            .join(GroupUsersORM)
            .filter(GroupUsersORM.user_id == user_id)
        )
        result = await self.__db_session.execute(stmt)
        return result.scalars().all()

    async def get_users_in_group(self, group_id: int) -> List[UserORM]:
        stmt = (
            select(UserORM)
            .join(GroupUsersORM)
            .filter(GroupUsersORM.group_id == group_id)
        )
        result = await self.__db_session.execute(stmt)
        return result.scalars().all()
