from app.core.config import settings
from app.domain.auth.schema import RegisterSSOUserSchema, SSOType
from app.domain.sso.base import BaseSSOClient
from app.domain.sso.google.config import GoogleSSOConfig
from app.domain.sso.google.google import GoogleSSOClient


class SSOService:
    def __init__(self) -> None:
        google_sso_client = GoogleSSOClient(
            config=GoogleSSOConfig(client_id=settings.GOOGLE_SSO_CLIENT_ID)
        )

        self.SSO_MAPPER = {SSOType.GOOGLE: google_sso_client}

    def get_client(self, provider: SSOType) -> BaseSSOClient:
        if provider in self.SSO_MAPPER:
            return self.SSO_MAPPER[provider]
