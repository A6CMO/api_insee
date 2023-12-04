#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from pathlib import Path
from typing import Any, Dict, Final

import pytest
from _pytest.fixtures import SubRequest

from api_insee import ApiInsee

PROJECT_ROOT: Final = Path(__file__).parent.parent


def parse_env_file() -> Dict[str, str]:
    with Path(PROJECT_ROOT, ".env").open() as file:
        lines = (
            line.split("=")
            for line in file.read().splitlines(keepends=False)
            if line and not line.startswith("#")
        )

        return {key.strip(): value.strip() for key, value in lines}


CREDENTIALS = parse_env_file()
SIRENE_API_CONSUMER_KEY = CREDENTIALS["SIRENE_API_CONSUMER_KEY"]
SIRENE_API_CONSUMER_SECRET = CREDENTIALS["SIRENE_API_CONSUMER_SECRET"]


@pytest.fixture
def api(request: SubRequest) -> ApiInsee:
    return ApiInsee(
        SIRENE_API_CONSUMER_KEY,
        SIRENE_API_CONSUMER_SECRET,
        noauth=request.config.option.record_mode is None,
    )


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


@pytest.fixture
def vcr_config() -> Dict[str, Any]:
    return {
        "filter_headers": ["authorization", "api_token", "Set-Cookie"],
        "before_record_response": replace_token,
    }
