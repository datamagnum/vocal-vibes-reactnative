from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.domain.user.schema import User
from app.infrastructure.postgres.models import Group as GroupORM
from app.infrastructure.postgres.models import GroupUsers as GroupUsersORM


class Group(BaseModel):
    id: str
    name: str
    description: str
    created_by: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    @classmethod
    def create_from_orm(cls, orm_obj: GroupORM) -> "Group":
        return cls(**orm_obj.__dict__)


class GroupUser(BaseModel):
    group_id: str
    user_id: int

    @classmethod
    def create_from_orm(cls, orm_obj: GroupUsersORM) -> "GroupUser":
        return cls(**orm_obj.__dict__)


class CreateGroupRequestSchema(BaseModel):
    name: str
    description: str = Field(default_factory=str)
    created_by: Optional[int] = None

    @property
    def orm_obj(self) -> "GroupORM":
        return GroupORM(
            name=self.name,
            description=self.description,
            created_by=self.created_by,
        )


class AddUserToGroupRequestSchema(BaseModel):
    user_id: int


class RemoveUserFromGroupRequestSchema(BaseModel):
    user_id: int


class ListUserGroupsResponseSchema(BaseModel):
    groups: List[Group]


class GetGroupRequestSchema(BaseModel):
    group_id: str


class ListUsersInGroupsResponseSchema(BaseModel):
    users: List[User]
