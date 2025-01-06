from typing import Any, cast

import pytest

from api_insee import ApiInsee, criteria

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

from tests.conftest import BASE_SIREN_URL


@pytest.mark.vcr
def test_siren_search(api: ApiInsee) -> None:
    request = api.siren("809893225")
    unit = cast(dict[str, Any], request.get())

    assert unit["uniteLegale"]["siren"] == "809893225"
    assert unit["header"]["statut"] == 200
    assert request.url == BASE_SIREN_URL + "/809893225"


@pytest.mark.vcr
def test_siren_raw_search(api: ApiInsee) -> None:
    criteria_ = criteria.Raw("unitePurgeeUniteLegale:True")
    request = api.siren(q=criteria_)
    results = cast(dict[str, Any], request.get())

    assert results["header"]["statut"] == 200
    assert request.url == BASE_SIREN_URL + "?q=unitePurgeeUniteLegale:True"


@pytest.mark.vcr
def test_siren_search_by_field(api: ApiInsee) -> None:
    criteria_ = criteria.Field("unitePurgeeUniteLegale", True)
    request = api.siren(q=criteria_)
    results = cast(dict[str, Any], request.get())

    assert results["header"]["statut"] == 200
    assert request.url == BASE_SIREN_URL + "?q=unitePurgeeUniteLegale:True"


def test_siren_search_date(api: ApiInsee) -> None:
    request = api.siren("005520135", date="2018-01-01")

    assert request.url == BASE_SIREN_URL + "/005520135?date=2018-01-01"


def test_siren_search_with_period_variable(api: ApiInsee) -> None:
    request = api.siren(q=criteria.PeriodicField("etatAdministratifUniteLegale", "C"))

    assert request.url == BASE_SIREN_URL + "?q=periode(etatAdministratifUniteLegale:C)"


def test_siren_search_exact_field(api: ApiInsee) -> None:
    request = api.siren(
        q=criteria.Periodic(
            criteria.FieldExact("denominationUniteLegale", "LE TIMBRE"),
        ),
    )

    assert (
        request.url
        == BASE_SIREN_URL + '?q=periode(denominationUniteLegale:"LE TIMBRE")'
    )


@pytest.mark.vcr
def test_siren_multi_unit(api: ApiInsee) -> None:
    request = api.siren(q={"categorieEntreprise": "PME"}, nombre=30)
    data = cast(dict[str, Any], request.get())

    sirens = [unit["siren"] for unit in data["unitesLegales"]]

    request = api.siren(sirens, nombre=30)
    data = cast(dict[str, Any], request.get())
    units = data["unitesLegales"]

    assert len(units) == 30
    for unit in units:
        assert unit["siren"] in sirens
