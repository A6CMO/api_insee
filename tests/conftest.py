#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib.util
import os
import re
import sys
from pathlib import Path
from typing import Any

import pytest

from api_insee import ApiInsee

#
#  Import API Insee Module
#

dir_path = os.path.dirname(os.path.realpath(__file__))
MODULE_PATH = dir_path + "/../src/api_insee/__init__.py"
MODULE_NAME = "api_insee"
spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def parse_env_file() -> dict[str, str]:
    with Path(Path(dir_path).parent, ".env").open() as file:
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
def api(request) -> ApiInsee:
    return ApiInsee(
        SIRENE_API_CONSUMER_KEY,
        SIRENE_API_CONSUMER_SECRET,
        noauth=request.config.option.record_mode is None,
    )


def replace_token(response: dict[str, Any]) -> dict[str, Any]:
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
def vcr_config():
    return {
        "filter_headers": ["authorization", "api_token", "Set-Cookie"],
        "before_record_response": replace_token,
    }
