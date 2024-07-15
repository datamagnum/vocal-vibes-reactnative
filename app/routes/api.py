from fastapi import APIRouter

from app.core.config import settings
from app.routes.endpoints.v1 import auth, group, session, topic, user

api_v1_router = APIRouter(prefix=f"{settings.API_V1_STR}")

api_v1_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_v1_router.include_router(user.router, prefix="/user", tags=["User"])
api_v1_router.include_router(topic.router, prefix="/topic", tags=["Topic"])
api_v1_router.include_router(session.router, prefix="/session", tags=["Session"])
api_v1_router.include_router(group.router, prefix="/group", tags=["Group"])
