import base64

from api_insee.exeptions.authentication_error import InvalidCredentialsError


class ClientCredentials:
    def __init__(self, key: str, secret: str) -> None:
        self.key = key
        self.secret = secret

        if not self.key or not self.secret:
            raise InvalidCredentialsError(self)

        self.encoded = self.get_encoded_credentials()

    def get_encoded_credentials(self) -> str:
        blike = f"{self.key}:{self.secret}".encode()

        return base64.b64encode(blike).decode("utf-8")
