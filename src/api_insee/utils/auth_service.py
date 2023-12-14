from typing import Callable

from api_insee.request.request_token import RequestTokenService
from api_insee.utils.client_credentials import ClientCredentials
from api_insee.utils.client_token import ClientToken, TokenProvider

RequestTokenServiceFactory = Callable[[ClientCredentials], RequestTokenService]


class AuthService:
    def __init__(
        self,
        key: str,
        secret: str,
        request_token_service_factory: RequestTokenServiceFactory,
    ) -> None:
        self.credentials = ClientCredentials(key=key, secret=secret)
        self.request_factory = request_token_service_factory
        self.token = self.get_token()

    def get_token(self) -> TokenProvider:
        data = self.request_factory(self.credentials).get(format="json")

        return ClientToken(**data)
