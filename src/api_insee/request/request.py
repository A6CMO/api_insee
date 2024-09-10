import json
import ssl
import urllib.error as ue
import urllib.parse as up
import urllib.request as ur

from http import HTTPStatus
from http.client import HTTPResponse
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    NoReturn,
    Optional,
    Tuple,
    Union,
    cast,
    overload,
)
from urllib.error import HTTPError

from api_insee import criteria
from api_insee.exceptions.request_error import RequestError, UrlError

if TYPE_CHECKING:
    from api_insee.conf import ApiPathName, ApiUrls
    from api_insee.utils.client_token import TokenProvider

AvailableFormat = Literal["csv", "json"]
AvailableMethod = Literal["get", "post"]


class RequestService:
    path_name: "ApiPathName"
    _accept_format = "application/json"

    def __init__(
        self,
        **kwargs: Union[
            Dict[str, Any],
            List[Any],
            Tuple[Any],
            str,
            float,
            criteria.Base,
        ],
    ) -> None:
        self._url_params: Dict[str, str] = {}
        self.token: Optional[TokenProvider] = None
        self.criteria: Optional[criteria.Base] = None
        self._api_urls: Optional[ApiUrls] = None

        for key, value in kwargs.items():
            self.set_url_params(key, value)

    def init_criteria_from_dictionnary(self, dictionnary: Dict[str, Any]) -> None:
        self.criteria = criteria.List(
            *[criteria.Field(key, value) for (key, value) in dictionnary.items()],
        )

    def init_criteria_from_criteria(self, *args: Any) -> None:
        self.criteria = criteria.List(*args)

    def use_token(self, token: "TokenProvider") -> None:
        self.token = token

    @overload
    def get(self) -> Dict[str, Any]: ...

    @overload
    def get(
        self,
        format: Optional[Literal["json"]] = None,
        method: AvailableMethod = "get",
    ) -> Dict[str, Any]: ...

    @overload
    def get(
        self,
        format: Literal["csv"],
        method: AvailableMethod = "get",
    ) -> str: ...

    def get(
        self,
        format: Optional[AvailableFormat] = None,
        method: AvailableMethod = "get",
    ) -> Union[str, Dict[str, Any]]:
        if format:
            self.format = format

        if method not in {"get", "post"}:
            msg = 'method parameter must be "get" or "post"'
            raise ValueError(msg)

        request = self.get_request() if method == "get" else self.post_request()
        if not request.full_url.startswith("https"):
            msg = f"invalid url {request.full_url}"
            raise ValueError(msg)

        ssl_context = ssl.create_default_context()

        try:
            response = ur.urlopen(request, context=ssl_context)  # noqa: S310

            return self.format_response(response)
        except ue.HTTPError as EX:
            self.catch_http_error(EX)
        except Exception as e:
            raise RequestError(self.url_encoded) from e

    def get_request(self) -> ur.Request:
        return self._create_request(self.url_encoded, self.data, self.header)

    def post_request(self) -> ur.Request:
        return self._create_request(
            self.url_path,
            up.urlencode(self._url_params).encode("utf-8"),
            {**self.header, "Content-Type": "application/x-www-form-urlencoded"},
        )

    def _create_request(
        self,
        url: str,
        data: Optional[bytes],
        headers: Dict[str, str],
    ) -> ur.Request:
        if not url.startswith("https"):
            msg = f"invalid url {url}"
            raise ValueError(msg)

        return ur.Request(url, data=data, headers=headers)  # noqa: S310

    def format_response(self, response: HTTPResponse) -> Union[str, Dict[str, Any]]:
        if self.format == "json":
            return self.format_response_json(response)

        if self.format == "csv":
            return self.format_response_csv(response)

        msg = f"Wrong response format {self.format}"
        raise ValueError(msg)

    def format_response_json(self, response: HTTPResponse) -> Dict[str, Any]:
        raw = response.read().decode("utf-8")

        return cast(Dict[str, Any], json.loads(raw))

    def format_response_csv(self, response: HTTPResponse) -> str:
        return response.read().decode("utf-8")

    @property
    def path(self) -> str:
        return self.api_urls[self.path_name]

    @property
    def api_urls(self) -> "ApiUrls":
        if self._api_urls is None:
            msg = "You need to set api_urls before send request"
            raise ValueError(msg)

        return self._api_urls

    @api_urls.setter
    def api_urls(self, value: "ApiUrls") -> None:
        self._api_urls = value

    @property
    def url(self) -> str:
        return up.unquote_plus(self.url_encoded)

    @property
    def url_encoded(self) -> str:
        return self.url_path + self.url_encoded_params

    @property
    def url_path(self) -> str:
        return self.path

    @property
    def url_encoded_params(self) -> str:
        params = up.urlencode(self.url_params, quote_via=up.quote_plus).split("&")
        encoded_params = "&".join(sorted(params))

        if encoded_params:
            return "?" + encoded_params

        return ""

    @property
    def url_params(self) -> Dict[str, str]:
        return self._url_params.copy()

    def set_url_params(
        self,
        name: str,
        value: Union[
            Dict[str, Any],
            List[Any],
            Tuple[Any],
            str,
            float,
            criteria.Base,
        ],
    ) -> None:
        if isinstance(value, dict):
            criteria_ = criteria.List(
                *[criteria.Field(key, value) for (key, value) in value.items()],
            ).to_url_params()

        elif isinstance(value, (list, tuple)):
            criteria_ = criteria.List(*value).to_url_params()

        elif isinstance(value, (float, int, str)):
            criteria_ = criteria.Raw(str(value)).to_url_params()

        elif isinstance(value, criteria.Base):
            criteria_ = value.to_url_params()

        else:
            raise TypeError

        self._url_params[name] = criteria_

    @property
    def data(self) -> Optional[bytes]:
        return None

    @property
    def header(self) -> Dict[str, str]:
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
        if error.code == HTTPStatus.BAD_REQUEST:
            raise UrlError(self)

        raise error
