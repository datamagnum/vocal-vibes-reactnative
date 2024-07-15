from google.auth.exceptions import InvalidValue, MalformedError
from google.auth.transport import requests
from google.oauth2 import id_token
from loguru import logger

from app.domain.auth.schema import RegisterSSOUserSchema, SSOType
from app.domain.sso.base import BaseSSOClient
from app.domain.sso.google.config import GoogleSSOConfig
from app.exceptions.exceptions_http import Unauthorized, Unauthorized_401


class GoogleSSOClient(BaseSSOClient):
    def __init__(self, config: GoogleSSOConfig) -> None:
        self._config = config

    async def validate_token(self, token: str) -> RegisterSSOUserSchema:
        try:
            id_info = id_token.verify_oauth2_token(
                token, requests.Request(), self._config.client_id
            )
        except (MalformedError, InvalidValue) as ex:
            logger.error(
                f"Error while trying verify session id token {str(ex) or repr(ex)}"
            )
            raise Unauthorized_401(
                ex=Unauthorized(
                    message=f"Error while trying verify session id token {str(ex) or repr(ex)}"
                )
            )

        return RegisterSSOUserSchema(
            first_name=id_info["given_name"],
            email=id_info["email"],
            sso_provider=SSOType.GOOGLE,
        )
