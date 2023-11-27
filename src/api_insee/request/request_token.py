from api_insee.conf import API_VERSION
from api_insee.exeptions.auth_exeption import AuthExeption
from .request import RequestService


class RequestTokenService(RequestService):
    def __init__(self, credentials):
        self.credentials = credentials

    @property
    def url_path(self):
        return API_VERSION["url"] + API_VERSION["path_token"]

    @property
    def data(self):
        return "grant_type=client_credentials".encode("ascii")

    @property
    def header(self):
        return {"Authorization": f"Basic {self.credentials.encoded}"}

    def catchHTTPError(self, error):
        if error.code == 401:
            raise AuthExeption(self.credentials).unauthorized(error.reason)

        return super().catchHTTPError(error)
