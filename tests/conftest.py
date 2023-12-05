import re

from typing import Any, Dict, Final, Type, Union
from unittest.mock import MagicMock

import pytest

from _pytest.fixtures import SubRequest
from api_insee import ApiInsee
from api_insee.conf import ApiVersion
from api_insee.utils.auth_service import AuthService
from utils import parse_env_file

CREDENTIALS: Final = parse_env_file()
SIRENE_API_CONSUMER_KEY: Final = CREDENTIALS["SIRENE_API_CONSUMER_KEY"]
SIRENE_API_CONSUMER_SECRET: Final = CREDENTIALS["SIRENE_API_CONSUMER_SECRET"]

API_VERSION: Final = ApiVersion.V_3
API_URLS: Final = API_VERSION.urls
BASE_SIREN_URL: Final = API_URLS["path_siren"]
BASE_SIRET_URL: Final = API_URLS["path_siret"]


@pytest.fixture()
def api(request: SubRequest) -> ApiInsee:
    return ApiInsee(
        SIRENE_API_CONSUMER_KEY,
        SIRENE_API_CONSUMER_SECRET,
        api_version=API_VERSION,
        auth_service=_get_auth_service(request),
    )


@pytest.fixture()
def api_311(request: SubRequest) -> ApiInsee:
    return ApiInsee(
        SIRENE_API_CONSUMER_KEY,
        SIRENE_API_CONSUMER_SECRET,
        api_version=ApiVersion.V_3_11,
        auth_service=_get_auth_service(request),
    )


def _get_auth_service(request: SubRequest) -> Union[Type[AuthService], MagicMock]:
    return (
        AuthService
        # We enable authentication when tests are launched in record mode
        if request.config.option.record_mode is not None
        else MagicMock()
    )


@pytest.fixture()
def vcr_config() -> Dict[str, Any]:
    return {
        "filter_headers": ["authorization", "api_token", "Set-Cookie"],
        "before_record_response": replace_token,
    }


def replace_token(response: Dict[str, Any]) -> Dict[str, Any]:
    if "headers" in response and "Set-Cookie" in response["headers"]:
        del response["headers"]["Set-Cookie"]

    if "body" in response and "string" in response["body"]:
        response["body"]["string"] = re.sub(
            b'"access_token":"[^"]+"',
            b'"access_token":"00000000-0000-0000-0000-000000000000"',
            response["body"]["string"],
        )

    return response
