from typing import Any, Final

import pytest

from api_insee import ApiInsee
from api_insee.conf import ApiVersion
from api_insee.request.request import RequestService
from tests.utils import parse_env_file

CREDENTIALS: Final = parse_env_file()
SIRENE_API_KEY: Final = CREDENTIALS["SIRENE_API_KEY"]

API_VERSION: Final = ApiVersion.V_3_11
API_URLS: Final = API_VERSION.urls
BASE_SIREN_URL: Final = API_URLS["path_siren"]
BASE_SIRET_URL: Final = API_URLS["path_siret"]


@pytest.fixture
def api() -> ApiInsee:
    return ApiInsee(SIRENE_API_KEY)


@pytest.fixture
def vcr_config() -> dict[str, Any]:
    return {
        "filter_headers": [RequestService.API_AUTHORIZATION_HEADER],
        "before_record_response": replace_token,
    }


def replace_token(response: dict[str, Any]) -> dict[str, Any]:
    if "headers" in response and "Set-Cookie" in response["headers"]:
        del response["headers"]["Set-Cookie"]

    return response
