from typing import Any, cast

import pytest

from api_insee import ApiInsee, criteria

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

from tests.conftest import BASE_SIRET_URL


@pytest.mark.vcr
def test_siret_search(api: ApiInsee) -> None:
    request = api.siret("39860733300059")
    unit = cast(dict[str, Any], request.get())

    assert unit["etablissement"]["siret"] == "39860733300059"
    assert unit["header"]["statut"] == 200
    assert request.url == BASE_SIRET_URL + "/39860733300059"


def test_siret_search_with_date(api: ApiInsee) -> None:
    request = api.siret("39860733300059", date="2015-08-01")
    assert request.url == BASE_SIRET_URL + "/39860733300059?date=2015-08-01"


def test_siret_search_with_champs(api: ApiInsee) -> None:
    champs = [
        "siret",
        "denominationUniteLegale",
        "nomUsageUniteLegale",
        "prenom1UniteLegale",
    ]

    request = api.siret("39860733300059", champs=champs)
    assert (
        request.url
        == BASE_SIRET_URL
        + "/39860733300059?champs=siret,denominationUniteLegale,nomUsageUniteLegale,prenom1UniteLegale"
    )


def test_siret_search_with_2_criteria(api: ApiInsee) -> None:
    request = api.siret(
        q=(
            criteria.Field("codeCommuneEtablissement", 92046),
            criteria.Field("unitePurgeeUniteLegale", True),
        ),
    )

    assert (
        request.url
        == BASE_SIRET_URL
        + "?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True"
    )


def test_siret_search_with_2_criteria_and_date(api: ApiInsee) -> None:
    request = api.siret(
        q=(
            criteria.Field("codeCommuneEtablissement", 92046),
            criteria.Field("unitePurgeeUniteLegale", True),
        ),
        date="2018-01-01",
    )

    assert (
        request.url
        == BASE_SIRET_URL
        + "?date=2018-01-01&q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True"
    )


def test_siret_search_from_dict_criteria(api: ApiInsee) -> None:
    request = api.siret(
        q={
            "unitePurgeeUniteLegale": True,
            "codeCommuneEtablissement": 92046,
        },
    )

    expected = {
        f"{BASE_SIRET_URL}?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True",
        f"{BASE_SIRET_URL}?q=unitePurgeeUniteLegale:True AND codeCommuneEtablissement:92046",
    }

    assert request.url in expected


def test_siret_search_with_operators_or_and_parentheses(api: ApiInsee) -> None:
    request = api.siret(
        q=(
            (
                criteria.Field("codeCommuneEtablissement", 92046)
                | criteria.Field("unitePurgeeUniteLegale", True)
            )
            & criteria.Field("codeCommuneEtablissement", 92046)
        ),
    )

    assert (
        request.url
        == BASE_SIRET_URL
        + "?q=codeCommuneEtablissement:92046 OR unitePurgeeUniteLegale:True AND codeCommuneEtablissement:92046"
    )


def test_siret_search_with_operators(api: ApiInsee) -> None:
    request = api.siret(
        q=criteria.Field("codeCommuneEtablissement", 92046)
        | criteria.Field("unitePurgeeUniteLegale", True),
    )

    assert (
        request.url
        == BASE_SIRET_URL
        + "?q=codeCommuneEtablissement:92046 OR unitePurgeeUniteLegale:True"
    )


def test_siret_search_with_not_operator(api: ApiInsee) -> None:
    request = api.siret(
        q=(
            -(-criteria.Field("codeCommuneEtablissement", 92046)),  # noqa: B002
            -criteria.Field("unitePurgeeUniteLegale", True),
        ),
    )

    assert (
        request.url
        == BASE_SIRET_URL
        + "?q=codeCommuneEtablissement:92046 AND -unitePurgeeUniteLegale:True"
    )


def test_siret_search_with_periodic_list(api: ApiInsee) -> None:
    request = api.siret(
        q=criteria.Periodic(
            criteria.Field("activitePrincipaleEtablissement", "84.23Z"),
            criteria.Field("etatAdministratifEtablissement", "A"),
        ),
    )
    assert (
        request.url
        == BASE_SIRET_URL
        + "?q=periode(activitePrincipaleEtablissement:84.23Z AND etatAdministratifEtablissement:A)"
    )


def test_siret_search_with_periodic_list_with_or(api: ApiInsee) -> None:
    request = api.siret(
        q=criteria.Periodic(
            criteria.Field("activitePrincipaleEtablissement", "84.23Z"),
            criteria.Field("activitePrincipaleEtablissement", "86.21Z"),
            criteria.Field("activitePrincipaleEtablissement", "87.21Z"),
            operator="OR",
        ),
    )

    assert (
        request.url
        == BASE_SIRET_URL
        + "?q=periode(activitePrincipaleEtablissement:84.23Z OR activitePrincipaleEtablissement:86.21Z OR activitePrincipaleEtablissement:87.21Z)"
    )


def test_siret_search_with_periodic_list_and_operators(api: ApiInsee) -> None:
    request = api.siret(
        q=criteria.Periodic(
            criteria.Field("activitePrincipaleEtablissement", "84.23Z")
            | criteria.Field("activitePrincipaleEtablissement", "86.21Z")
            & criteria.Field("etatAdministratifEtablissement", "A"),
        ),
    )

    assert (
        request.url
        == BASE_SIRET_URL
        + "?q=periode(activitePrincipaleEtablissement:84.23Z OR activitePrincipaleEtablissement:86.21Z AND etatAdministratifEtablissement:A)"
    )


def test_siret_search_with_periodic_list_and_operators_excluding(api: ApiInsee) -> None:
    request = api.siret(
        q=criteria.Periodic(
            criteria.Field("activitePrincipaleEtablissement", "84.23Z")
            | criteria.Field("activitePrincipaleEtablissement", "86.21Z"),
        )
        & criteria.PeriodicField("etatAdministratifEtablissement", "A"),
    )

    assert (
        request.url
        == BASE_SIRET_URL
        + "?q=periode(activitePrincipaleEtablissement:84.23Z OR activitePrincipaleEtablissement:86.21Z) AND periode(etatAdministratifEtablissement:A)"
    )


def test_siret_search_with_including_borne(api: ApiInsee) -> None:
    request = api.siret(q=criteria.Range("nomUsageUniteLegale", "DUPONT", "DURANT"))

    assert request.url == BASE_SIRET_URL + "?q=nomUsageUniteLegale:[DUPONT TO DURANT]"


def test_siret_search_with_excluding_borne(api: ApiInsee) -> None:
    request = api.siret(
        q=criteria.Range("nomUsageUniteLegale", "DUPONT", "DURANT", exclude=True),
    )

    assert request.url == BASE_SIRET_URL + "?q=nomUsageUniteLegale:{DUPONT TO DURANT}"


@pytest.mark.vcr
def test_siret_multi_unit(api: ApiInsee) -> None:
    request = api.siret(q="codeCommuneEtablissement:92046", nombre=1000)
    data = cast(dict[str, Any], request.get())

    _list = []
    for unit in data["etablissements"]:
        _list.append(unit["siret"])

    request = api.siret(_list, nombre=1000)
    data = cast(dict[str, Any], request.get())
    units = data["etablissements"]

    assert len(units) == 1000
    for unit in units:
        assert unit["siret"] in _list
