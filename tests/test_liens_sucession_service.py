#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from api_insee import criteria
from api_insee.conf import API_VERSION

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

base_siret_url = API_VERSION["url"] + API_VERSION["path_siret"]


def test_liens_succession_search(api):
    request = api.liens_succession(
        q=criteria.Field("siretEtablissementPredecesseur", 39860733300042)
    )
    assert (
        request.url
        == base_siret_url
        + "/liensSuccession?q=siretEtablissementPredecesseur:39860733300042"
    )

    request = api.liens_succession(
        q=(
            criteria.Field("siretEtablissementPredecesseur", "00555008200027")
            & criteria.Field("dateLienSuccession", "2004-04-01")
        )
    )
    assert (
        request.url
        == base_siret_url
        + "/liensSuccession?q=siretEtablissementPredecesseur:00555008200027 AND dateLienSuccession:2004-04-01"
    )


@pytest.mark.vcr
def test_liens_succession_search_request(api):
    request = api.liens_succession(
        q=criteria.Field("siretEtablissementPredecesseur", 39860733300042)
    )
    data = request.get()
    siret_predecesseur = data["liensSuccession"][0]["siretEtablissementPredecesseur"]

    assert siret_predecesseur == "39860733300042"

    request = api.liens_succession(
        q=(
            criteria.Field("siretEtablissementPredecesseur", "00555008200027")
            & criteria.Field("dateLienSuccession", "2004-04-01")
        )
    )
    data = request.get()
    siret_predecesseur = data["liensSuccession"][0]["siretEtablissementPredecesseur"]
    assert siret_predecesseur == "00555008200027"
    assert data["liensSuccession"][0]["dateLienSuccession"] == "2004-04-01"
