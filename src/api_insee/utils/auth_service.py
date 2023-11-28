from typing import Optional

from api_insee.request.request_token import RequestTokenService
from api_insee.utils.client_credentials import ClientCredentials
from api_insee.utils.client_token import ClientToken


class AuthService:
    def __init__(self, key: Optional[str] = None, secret: Optional[str] = None) -> None:
        self.credentials = ClientCredentials(key=key, secret=secret)
        self.token = self.get_token()

    def get_token(self) -> ClientToken:
        data = RequestTokenService(self.credentials).get(format="json")
        return ClientToken(**data)


class MockAuth(AuthService):
    def get_token(self) -> ClientToken:
        return ClientToken(
            token_type="Bearer",
            expires_in=100000,
            access_token="No Auth",
            scope="No Scope",
        )
