from api_insee.request.request_token import RequestTokenService
from api_insee.utils.client_credentials import ClientCredentials
from api_insee.utils.client_token import ClientToken


class AuthService:
    token = None

    def __init__(self, key=False, secret=False):
        self.credentials = ClientCredentials(key=key, secret=secret)
        self.generate_token()

    def generate_token(self) -> None:
        data = RequestTokenService(self.credentials).get()
        self.token = ClientToken(**data)


class MockAuth(AuthService):
    def __init__(self):
        self.token = ClientToken(
            token_type="Bearer",
            expires_in=100000,
            access_token="No Auth",
            scope="No Scope",
        )
