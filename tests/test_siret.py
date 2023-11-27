#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from api_insee import criteria
from api_insee.conf import API_VERSION

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

base_siret_url = API_VERSION["url"] + API_VERSION["path_siret"]


@pytest.mark.vcr
def test_siret_search(api):
    request = api.siret("39860733300059")
    unit = request.get()

    assert unit["etablissement"]["siret"] == "39860733300059"
    assert unit["header"]["statut"] == 200
    assert request.url == base_siret_url + "/39860733300059"


def test_siret_search_with_date(api):
    request = api.siret("39860733300059", date="2015-08-01")
    assert request.url == base_siret_url + "/39860733300059?date=2015-08-01"


def test_siret_search_with_champs(api):
    champs = [
        "siret",
        "denominationUniteLegale",
        "nomUsageUniteLegale",
        "prenom1UniteLegale",
    ]

    request = api.siret("39860733300059", champs=champs)
    assert (
        request.url
        == base_siret_url
        + "/39860733300059?champs=siret,denominationUniteLegale,nomUsageUniteLegale,prenom1UniteLegale"
    )


def test_siret_search_with_2_criteria(api):
    request = api.siret(
        q=(
            criteria.Field("codeCommuneEtablissement", 92046),
            criteria.Field("unitePurgeeUniteLegale", True),
        )
    )

    assert (
        request.url
        == base_siret_url
        + "?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True"
    )


def test_siret_search_with_2_criteria_and_date(api):
    request = api.siret(
        q=(
            criteria.Field("codeCommuneEtablissement", 92046),
            criteria.Field("unitePurgeeUniteLegale", True),
        ),
        date="2018-01-01",
    )

    assert (
        request.url
        == base_siret_url
        + "?date=2018-01-01&q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True"
    )


def test_siret_search_from_dic_criteria(api):
    request = api.siret(
        q={"unitePurgeeUniteLegale": True, "codeCommuneEtablissement": 92046}
    )

    assert (
        request.url
        == base_siret_url
        + "?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True"
        or request.url
        == base_siret_url
        + "?q=unitePurgeeUniteLegale:True AND codeCommuneEtablissement:92046"
    )


def test_siret_search_with_operators_or_and_parentheses(api):
    request = api.siret(
        q=(
            (
                criteria.Field("codeCommuneEtablissement", 92046)
                | criteria.Field("unitePurgeeUniteLegale", True)
            )
            & criteria.Field("codeCommuneEtablissement", 92046)
        )
    )

    assert (
        request.url
        == base_siret_url
        + "?q=codeCommuneEtablissement:92046 OR unitePurgeeUniteLegale:True AND codeCommuneEtablissement:92046"
    )


def test_siret_search_with_operators(api):
    request = api.siret(
        q=criteria.Field("codeCommuneEtablissement", 92046)
        | criteria.Field("unitePurgeeUniteLegale", True)
    )

    assert (
        request.url
        == base_siret_url
        + "?q=codeCommuneEtablissement:92046 OR unitePurgeeUniteLegale:True"
    )


def test_siret_search_with_not_operator(api):
    request = api.siret(
        q=(
            -(-criteria.Field("codeCommuneEtablissement", 92046)),
            -criteria.Field("unitePurgeeUniteLegale", True),
        )
    )

    assert (
        request.url
        == base_siret_url
        + "?q=codeCommuneEtablissement:92046 AND -unitePurgeeUniteLegale:True"
    )


def test_siret_search_with_periodic_list(api):
    request = api.siret(
        q=criteria.Periodic(
            criteria.Field("activitePrincipaleEtablissement", "84.23Z"),
            criteria.Field("etatAdministratifEtablissement", "A"),
        )
    )
    assert (
        request.url
        == base_siret_url
        + "?q=periode(activitePrincipaleEtablissement:84.23Z AND etatAdministratifEtablissement:A)"
    )


def test_siret_search_with_periodic_list_with_or(api):
    request = api.siret(
        q=criteria.Periodic(
            criteria.Field("activitePrincipaleEtablissement", "84.23Z"),
            criteria.Field("activitePrincipaleEtablissement", "86.21Z"),
            criteria.Field("activitePrincipaleEtablissement", "87.21Z"),
            operator="OR",
        )
    )

    assert (
        request.url
        == base_siret_url
        + "?q=periode(activitePrincipaleEtablissement:84.23Z OR activitePrincipaleEtablissement:86.21Z OR activitePrincipaleEtablissement:87.21Z)"
    )


def test_siret_search_with_periodic_list_and_operators(api):
    request = api.siret(
        q=criteria.Periodic(
            criteria.Field("activitePrincipaleEtablissement", "84.23Z")
            | criteria.Field("activitePrincipaleEtablissement", "86.21Z")
            & criteria.Field("etatAdministratifEtablissement", "A")
        )
    )

    assert (
        request.url
        == base_siret_url
        + "?q=periode(activitePrincipaleEtablissement:84.23Z OR activitePrincipaleEtablissement:86.21Z AND etatAdministratifEtablissement:A)"
    )


def test_siret_search_with_periodic_list_and_operators_excluding(api):
    request = api.siret(
        q=criteria.Periodic(
            criteria.Field("activitePrincipaleEtablissement", "84.23Z")
            | criteria.Field("activitePrincipaleEtablissement", "86.21Z")
        )
        & criteria.PeriodicField("etatAdministratifEtablissement", "A")
    )

    assert (
        request.url
        == base_siret_url
        + "?q=periode(activitePrincipaleEtablissement:84.23Z OR activitePrincipaleEtablissement:86.21Z) AND periode(etatAdministratifEtablissement:A)"
    )


def test_siret_search_with_including_borne(api):
    request = api.siret(q=criteria.Range("nomUsageUniteLegale", "DUPONT", "DURANT"))

    assert request.url == base_siret_url + "?q=nomUsageUniteLegale:[DUPONT TO DURANT]"


def test_siret_search_with_excluding_borne(api):
    request = api.siret(
        q=criteria.Range("nomUsageUniteLegale", "DUPONT", "DURANT", exclude=True)
    )

    assert request.url == base_siret_url + "?q=nomUsageUniteLegale:{DUPONT TO DURANT}"


@pytest.mark.vcr
def test_siret_multi_unit(api):
    data = api.siret(q="codeCommuneEtablissement:92046", nombre=1000).get()

    _list = []
    for unit in data["etablissements"]:
        _list.append(unit["siret"])

    data = api.siret(_list, nombre=1000)
    data = data.get()
    units = data["etablissements"]

    assert len(units) == 1000
    for unit in units:
        assert unit["siret"] in _list
