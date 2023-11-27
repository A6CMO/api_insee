#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

import conftest as conf
from api_insee import ApiInsee
from api_insee.exeptions.auth_exeption import AuthExeption

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"


def test_missing_credentials():
    with pytest.raises(AuthExeption):
        api = ApiInsee(False, False)


@pytest.mark.vcr
def test_unauthorized_credentials():
    with pytest.raises(AuthExeption):
        api = ApiInsee(
            key='wrong api key',
            secret=conf.SIRENE_API_CONSUMER_SECRET,
        )


@pytest.mark.vcr
def test_generate_token():
    api = ApiInsee(
        key=conf.SIRENE_API_CONSUMER_KEY,
        secret=conf.SIRENE_API_CONSUMER_SECRET,
    )

    assert len(api.auth.token.access_token) > 0
