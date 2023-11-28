from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from api_insee.request.request import RequestService


class RequestError(Exception):
    pass


class UrlError(RequestError):
    def __init__(self, request: "RequestService") -> None:
        super().__init__(f"bad request url : {request.url}")
