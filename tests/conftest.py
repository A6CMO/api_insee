import re

from typing import Any, Dict, Type

import pytest

from _pytest.fixtures import SubRequest
from api_insee import ApiInsee
from utils import ApiInseeTestDouble, parse_env_file

CREDENTIALS = parse_env_file()
SIRENE_API_CONSUMER_KEY = CREDENTIALS["SIRENE_API_CONSUMER_KEY"]
SIRENE_API_CONSUMER_SECRET = CREDENTIALS["SIRENE_API_CONSUMER_SECRET"]


@pytest.fixture()
def api(request: SubRequest) -> ApiInsee:
    api_insee: Type[ApiInsee] = (
        ApiInsee
        if request.config.option.record_mode is not None
        else ApiInseeTestDouble
    )

    return api_insee(
        SIRENE_API_CONSUMER_KEY,
        SIRENE_API_CONSUMER_SECRET,
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
