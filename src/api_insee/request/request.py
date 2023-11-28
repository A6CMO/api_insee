import json
import ssl
import urllib.error as ue
import urllib.parse as up
import urllib.request as ur
from http.client import HTTPResponse
from typing import Any, Literal, NoReturn, Optional, Union, cast, overload
from urllib.error import HTTPError

from api_insee import criteria
from api_insee.exeptions.request_error import UrlError
from api_insee.utils.client_token import ClientToken

AvailableFormat = Literal["csv", "json"]
AvailableMethod = Literal["get", "post"]


class RequestService:
    _accept_format = "application/json"

    def __init__(
        self,
        *args: Any,
        **kwargs: Union[
            dict[str, Any],
            list[Any],
            tuple[Any],
            str,
            int,
            float,
            criteria.Base,
        ],
    ) -> None:
        self._url_params: dict[str, str] = {}
        self.token: Optional[ClientToken] = None
        self.criteria: Optional[criteria.Base] = None

        for key, value in kwargs.items():
            self.set_url_params(key, value)

    def init_criteria_from_dictionnary(self, dictionnary: dict[str, Any]) -> None:
        self.criteria = criteria.List(
            *[criteria.Field(key, value) for (key, value) in dictionnary.items()]
        )

    def init_criteria_from_criteria(self, *args: Any) -> None:
        self.criteria = criteria.List(*args)

    def use_token(self, token: ClientToken) -> None:
        self.token = token

    @overload
    def get(
        self,
        format: Optional[Literal["json"]],
        method: AvailableMethod = "get",
    ) -> dict[str, Any]:
        ...

    @overload
    def get(
        self,
        format: Literal["csv"],
        method: AvailableMethod = "get",
    ) -> str:
        ...

    def get(
        self,
        format: Optional[AvailableFormat] = None,
        method: AvailableMethod = "get",
    ) -> Union[str, dict[str, Any]]:
        if format:
            self.format = format

        if method not in {"get", "post"}:
            msg = f'method parameter must be "get" or "post"'
            raise ValueError(msg)

        try:
            request = self.get_request() if method == "get" else self.post_request()
            gcontext = ssl.SSLContext()
            response = ur.urlopen(request, context=gcontext)

            return self.format_response(response)
        except ue.HTTPError as EX:
            self.catch_http_error(EX)
        except Exception:
            raise Exception(self.url_encoded)

    def get_request(self) -> ur.Request:
        return ur.Request(self.url_encoded, data=self.data, headers=self.header)

    def post_request(self) -> ur.Request:
        header = self.header
        header.update({"Content-Type": "application/x-www-form-urlencoded"})
        data = up.urlencode(self._url_params).encode("utf-8")

        return ur.Request(self.url_path, data=data, headers=header)

    def format_response(self, response: HTTPResponse) -> Union[str, dict[str, Any]]:
        if self.format == "json":
            return self.format_response_json(response)

        if self.format == "csv":
            return self.format_response_csv(response)

    def format_response_json(self, response: HTTPResponse) -> dict[str, Any]:
        raw = response.read().decode("utf-8")
        parsed = cast(dict[str, Any], json.loads(raw))

        return parsed

    def format_response_csv(self, response: HTTPResponse) -> str:
        raw = response.read().decode("utf-8")

        return raw

    @property
    def url(self) -> str:
        return up.unquote_plus(self.url_encoded)

    @property
    def url_encoded(self) -> str:
        return self.url_path + self.url_encoded_params

    @property
    def url_path(self) -> str:
        return "/"

    @property
    def url_encoded_params(self) -> str:
        params = up.urlencode(self.url_params, quote_via=up.quote_plus).split("&")
        encoded_params = "&".join(sorted(params))

        if encoded_params:
            return "?" + encoded_params

        return ""

    @property
    def url_params(self) -> dict[str, str]:
        return self._url_params.copy()

    def set_url_params(
        self,
        name: str,
        value: Union[
            dict[str, Any],
            list[Any],
            tuple[Any],
            str,
            int,
            float,
            criteria.Base,
        ],
    ) -> None:
        if isinstance(value, dict):
            criteria_ = criteria.List(
                *[criteria.Field(key, value) for (key, value) in value.items()]
            ).to_url_params()

        elif isinstance(value, list) or isinstance(value, tuple):
            criteria_ = criteria.List(*value).to_url_params()

        elif (
            isinstance(value, str) or isinstance(value, int) or isinstance(value, float)
        ):
            criteria_ = criteria.Raw(str(value)).to_url_params()

        elif isinstance(value, criteria.Base):
            criteria_ = value.to_url_params()

        else:
            raise Exception

        self._url_params[name] = criteria_

    @property
    def data(self) -> Optional[bytes]:
        return None

    @property
    def header(self) -> dict[str, str]:
        if not self.token:
            msg = "Token is not set"
            raise ValueError(msg)

        return {
            "Accept": self._accept_format,
            "Authorization": f"Bearer {self.token.access_token}",
        }

    @property
    def format(self) -> AvailableFormat:
        if self._accept_format == "application/json":
            return "json"

        if self._accept_format == "text/csv":
            return "csv"

        msg = f'"{self._accept_format}" not in available format ("csv", "json").'
        raise ValueError(msg)

    @format.setter
    def format(self, value: AvailableFormat) -> None:
        if value == "csv":
            self._accept_format = "text/csv"
        if value == "json":
            self._accept_format = "application/json"

    def catch_http_error(self, error: HTTPError) -> NoReturn:
        if error.code == 400:
            raise UrlError(self)

        raise error
