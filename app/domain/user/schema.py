from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.infrastructure.postgres.models import User as UserORM


class User(BaseModel):
    id: int
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    email: str
    password: Optional[str] = Field(exclude=True)
    sso_provider: Optional[str]
    traits: dict
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create_from_orm(cls, orm_obj: UserORM) -> "User":
        return cls(**orm_obj.__dict__)


class ListUserResponseSchema(BaseModel):
    users: List[User]
