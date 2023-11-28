from typing import NoReturn
from urllib.error import HTTPError

from api_insee.conf import API_VERSION
from api_insee.exeptions.authentication_error import InvalidCredentialsError
from api_insee.utils.client_credentials import ClientCredentials
from .request import RequestService


class RequestTokenService(RequestService):
    def __init__(self, credentials: ClientCredentials) -> None:
        super().__init__()
        self.credentials = credentials

    @property
    def url_path(self) -> str:
        return API_VERSION["url"] + API_VERSION["path_token"]

    @property
    def data(self) -> bytes:
        return "grant_type=client_credentials".encode("ascii")

    @property
    def header(self) -> dict[str, str]:
        return {"Authorization": f"Basic {self.credentials.encoded}"}

    def catch_http_error(self, error: HTTPError) -> NoReturn:
        if error.code == 401:
            raise InvalidCredentialsError(self.credentials)

        super().catch_http_error(error)
