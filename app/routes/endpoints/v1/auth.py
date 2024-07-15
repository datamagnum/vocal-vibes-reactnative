from fastapi import APIRouter, Depends
from starlette import status

from app.domain.auth.schema import (
    AuthSSOSchema,
    LoginUserSchema,
    RefreshTokenRequestSchema,
    RegisterUserSchema,
    TokenResponse,
)
from app.domain.auth.service import AuthService
from app.exceptions.exceptions_http import DuplicateEntityError, Unauthorized_401
from app.exceptions.exceptions_internal import (
    DuplicateEntity,
    EntityNotFound,
    Unauthorized,
)
from app.infrastructure.postgres.models import User
from app.routes.deps.security import renew_access_token
from app.routes.servicesfac import get_auth_service

router = APIRouter()


@router.post(
    "/register",
)
async def register(
    payload: RegisterUserSchema, auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return await auth_service.register_user(payload=payload)
    except DuplicateEntity as ex:
        raise DuplicateEntityError(ex=ex)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginUserSchema, auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    try:
        return await auth_service.authenticate_user(payload=payload)
    except Unauthorized as ex:
        raise Unauthorized_401(ex=ex)


@router.post("/sso/login", response_model=TokenResponse)
async def login_sso(
    payload: AuthSSOSchema, auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    try:
        return await auth_service.authenticate_user_by_sso(payload=payload)
    except Unauthorized as ex:
        raise Unauthorized_401(ex=ex)


@router.post(
    "/sso/register",
)
async def register_sso(
    payload: AuthSSOSchema, auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return await auth_service.register_user_by_sso(payload=payload)
    except DuplicateEntity as ex:
        raise DuplicateEntityError(ex=ex)


@router.post(
    "/token/refresh",
)
async def refresh_access_token(
    payload: RefreshTokenRequestSchema,
    access_token: str = Depends(renew_access_token),
) -> TokenResponse:
    return TokenResponse(access_token=access_token, refresh_token=payload.refresh_token)
