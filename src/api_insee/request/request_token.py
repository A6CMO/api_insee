from http import HTTPStatus
from typing import Dict, NoReturn
from urllib.error import HTTPError

from api_insee.exceptions.authentication_error import InvalidCredentialsError
from api_insee.utils.client_credentials import ClientCredentials

from .request import RequestService


class RequestTokenService(RequestService):
    path_name = "path_token"

    def __init__(self, credentials: ClientCredentials) -> None:
        super().__init__()
        self.credentials = credentials

    @property
    def data(self) -> bytes:
        return "grant_type=client_credentials".encode("ascii")

    @property
    def header(self) -> Dict[str, str]:
        return {"Authorization": f"Basic {self.credentials.encoded}"}

    def catch_http_error(self, error: HTTPError) -> NoReturn:
        if error.code == HTTPStatus.UNAUTHORIZED:
            raise InvalidCredentialsError(self.credentials)

        super().catch_http_error(error)
