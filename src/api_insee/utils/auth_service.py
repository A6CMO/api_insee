from api_insee.request.request_token import RequestTokenService
from api_insee.utils.client_credentials import ClientCredentials
from api_insee.utils.client_token import ClientToken


class AuthService:
    def __init__(self, key: str, secret: str) -> None:
        self.credentials = ClientCredentials(key=key, secret=secret)
        self.token = self.get_token()

    def get_token(self) -> ClientToken:
        data = RequestTokenService(self.credentials).get(format="json")
        return ClientToken(**data)
