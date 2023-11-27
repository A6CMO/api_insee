#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

import pytest

import api_insee.criteria as Criteria
import conftest as conf
from api_insee import ApiInsee
from api_insee.conf import API_VERSION
from api_insee.exeptions.request_exeption import RequestExeption

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

base_siren_url = API_VERSION["url"] + API_VERSION["path_siren"]


@pytest.mark.vcr
def test_request_format_fallback_is_json(api):
    request = api.siret("39860733300059")
    assert request.header["Accept"] == "application/json"


@pytest.mark.vcr
def test_request_format_fallback_is_csv(api):
    api_csv = ApiInsee(
        key=conf.SIRENE_API_CONSUMER_KEY,
        secret=conf.SIRENE_API_CONSUMER_SECRET,
        format="csv",
    )

    request = api_csv.siret("39860733300059")
    assert request.header["Accept"] == "text/csv"


@pytest.mark.vcr
def test_request_format_csv(api):
    request = api.siret(
        q='denominationUniteLegale:"bleu le"&nombre=20&champs=denominationUniteLegale'
    )
    request.format = "csv"

    assert request.header["Accept"] == "text/csv"


@pytest.mark.vcr
def test_request_format_csv_in_get_parameters(api):
    request = api.siret(
        q=(
            Criteria.Field("codeCommuneEtablissement", 92046),
            Criteria.Field("unitePurgeeUniteLegale", True),
        )
    )
    data = request.get(format="csv")
    reader = csv.reader(data.split("\n"), delimiter=",")

    assert request.header["Accept"] == "text/csv"

    lcount = 0
    for row in reader:
        assert "siren" in row
        lcount += 1
        break

    assert lcount == 1


@pytest.mark.vcr
def test_request_csv_fail_with_cursor(api):
    request = api.siren(Criteria.Raw("*"))
    request.format = "csv"

    assert request.header["Accept"] == "text/csv"

    with pytest.raises(RequestExeption):
        pages = request.pages()
        first = next(pages)
