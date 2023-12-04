#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Dict, cast

import pytest

from api_insee import ApiInsee, criteria
from api_insee.conf import API_VERSION

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

base_siren_url = API_VERSION["url"] + API_VERSION["path_siren"]


@pytest.mark.vcr
def test_siren_search(api: ApiInsee) -> None:
    request = api.siren("809893225")
    unit = cast(Dict[str, Any], request.get())

    assert unit["uniteLegale"]["siren"] == "809893225"
    assert unit["header"]["statut"] == 200
    assert request.url == base_siren_url + "/809893225"


@pytest.mark.vcr
def test_siren_raw_search(api: ApiInsee) -> None:
    criteria_ = criteria.Raw("unitePurgeeUniteLegale:True")
    request = api.siren(q=criteria_)
    results = cast(Dict[str, Any], request.get())

    assert results["header"]["statut"] == 200
    assert request.url == base_siren_url + "?q=unitePurgeeUniteLegale:True"


@pytest.mark.vcr
def test_siren_search_by_field(api: ApiInsee) -> None:
    criteria_ = criteria.Field("unitePurgeeUniteLegale", True)
    request = api.siren(q=criteria_)
    results = cast(Dict[str, Any], request.get())

    assert results["header"]["statut"] == 200
    assert request.url == base_siren_url + "?q=unitePurgeeUniteLegale:True"


def test_siren_search_date(api: ApiInsee) -> None:
    request = api.siren("005520135", date="2018-01-01")

    assert request.url == base_siren_url + "/005520135?date=2018-01-01"


def test_siren_search_with_period_variable(api: ApiInsee) -> None:
    request = api.siren(q=criteria.PeriodicField("etatAdministratifUniteLegale", "C"))

    assert request.url == base_siren_url + "?q=periode(etatAdministratifUniteLegale:C)"


def test_siren_search_exact_field(api: ApiInsee) -> None:
    request = api.siren(
        q=criteria.Periodic(criteria.FieldExact("denominationUniteLegale", "LE TIMBRE"))
    )

    assert (
        request.url
        == base_siren_url + '?q=periode(denominationUniteLegale:"LE TIMBRE")'
    )


@pytest.mark.vcr
def test_siren_multi_unit(api: ApiInsee) -> None:
    request = api.siren(q={"categorieEntreprise": "PME"}, nombre=1000)
    data = cast(Dict[str, Any], request.get())

    _list = []
    for unit in data["unitesLegales"]:
        _list.append(unit["siren"])

    request = api.siren(_list, nombre=1000)
    data = cast(Dict[str, Any], request.get())
    units = data["unitesLegales"]

    assert len(units) == 1000
    for unit in units:
        assert unit["siren"] in _list
