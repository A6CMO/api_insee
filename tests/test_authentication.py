#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

import conftest as conf
from api_insee import ApiInsee

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

from api_insee.exeptions.authentication_error import InvalidCredentialsError


def test_missing_credentials() -> None:
    with pytest.raises(InvalidCredentialsError):
        ApiInsee(None, None)


@pytest.mark.vcr
def test_unauthorized_credentials() -> None:
    with pytest.raises(InvalidCredentialsError):
        ApiInsee(
            key="wrong api key",
            secret=conf.SIRENE_API_CONSUMER_SECRET,
        )


@pytest.mark.vcr
def test_generate_token() -> None:
    api = ApiInsee(
        key=conf.SIRENE_API_CONSUMER_KEY,
        secret=conf.SIRENE_API_CONSUMER_SECRET,
    )

    assert api.auth.token.access_token
