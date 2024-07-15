from enum import Enum

from pydantic import BaseModel

from app.core.security import get_password_hash
from app.infrastructure.postgres.models import User as UserORM


class SSOType(str, Enum):
    GOOGLE = "GOOGLE"
    FACEBOOK = "FACEBOOK"


class RegisterUserSchema(BaseModel):
    email: str
    password: str
    first_name: str

    @property
    def orm_obj(self) -> UserORM:
        return UserORM(
            email=self.email,
            password=get_password_hash(password=self.password),
            first_name=self.first_name,
        )

    # @classmethod
    # def create_from_orm(cls, orm_obj: UserORM) -> "User":
    #     return cls(id=orm_obj.user_id, email=orm_obj.email)


class RegisterSSOUserSchema(BaseModel):
    email: str
    first_name: str
    sso_provider: SSOType

    @property
    def orm_obj(self) -> UserORM:
        return UserORM(
            email=self.email, first_name=self.first_name, sso_provider=self.sso_provider
        )


class LoginUserSchema(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class AuthSSOSchema(BaseModel):
    id_token: str
    sso_type: SSOType


class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str
