from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import scoped_session

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.domain.auth.schema import (
    AuthSSOSchema,
    LoginUserSchema,
    RefreshTokenRequestSchema,
    RegisterUserSchema,
    TokenResponse,
)
from app.domain.sso.service import SSOService
from app.exceptions.exceptions_http import Unauthorized_401
from app.exceptions.exceptions_internal import (
    DuplicateEntity,
    EntityNotFound,
    Unauthorized,
)
from app.infrastructure.postgres.queries.user import UserQueries

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db_session: scoped_session, sso_service: SSOService) -> None:
        self.__user_queries: UserQueries = UserQueries(db_session=db_session)
        self._sso_service: SSOService = sso_service

    async def register_user(self, payload: RegisterUserSchema) -> Any:
        user_orm = await self.__user_queries.get_by_email(email=payload.email)

        if user_orm:
            raise DuplicateEntity(
                entity="User",
                id=payload.email,
                readable_message="Authentication Failed: Invalid Credentials",
            )

        user = await self.__user_queries.create(user=payload.orm_obj)
        return user

    async def register_user_by_sso(self, payload: AuthSSOSchema) -> Any:
        sso_client = self._sso_service.get_client(provider=payload.sso_type)
        sso_user = await sso_client.validate_token(token=payload.id_token)

        user_orm = await self.__user_queries.get_by_email(email=sso_user.email)

        if user_orm:
            raise DuplicateEntity(
                entity="User",
                id=sso_user.email,
                readable_message="User already exist",
            )

        user = await self.__user_queries.create(user=sso_user.orm_obj)
        return user

    async def authenticate_user_by_sso(self, payload: AuthSSOSchema) -> TokenResponse:
        sso_client = self._sso_service.get_client(provider=payload.sso_type)
        sso_user = await sso_client.validate_token(token=payload.id_token)

        user_orm = await self.__user_queries.get_by_email(email=sso_user.email)

        if not user_orm or user_orm.sso_provider != payload.sso_type:
            raise Unauthorized(
                message="Authentication Failed",
                readable_message="Authentication Failed: Invalid Credentials",
            )

        access_token = create_access_token(sso_user.email)
        refresh_token = create_refresh_token(sso_user.email)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def authenticate_user(self, payload: LoginUserSchema) -> TokenResponse:
        user_orm = await self.__user_queries.get_by_email(email=payload.email)

        if not user_orm:
            raise Unauthorized(
                message="Authentication Failed",
                readable_message="Authentication Failed: Invalid Credentials",
            )

        if not verify_password(
            plain_password=payload.password, hashed_password=user_orm.password
        ):
            raise Unauthorized(
                message="Authentication Failed",
                readable_message="Authentication Failed: Invalid Credentials",
            )

        access_token = create_access_token(payload.email)
        refresh_token = create_refresh_token(payload.email)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
