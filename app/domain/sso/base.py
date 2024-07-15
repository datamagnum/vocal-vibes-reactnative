from abc import ABC

from app.domain.auth.schema import RegisterSSOUserSchema


class BaseSSOClient(ABC):
    async def validate_token(self, token: str) -> RegisterSSOUserSchema:
        ...
