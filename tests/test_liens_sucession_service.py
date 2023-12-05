from typing import Any, Dict, cast

import pytest

from api_insee import ApiInsee, criteria

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

from conftest import BASE_SIRET_URL


def test_liens_succession_search(api: ApiInsee) -> None:
    request = api.liens_succession(
        q=criteria.Field("siretEtablissementPredecesseur", 39860733300042),
    )
    assert (
        request.url
        == BASE_SIRET_URL
        + "/liensSuccession?q=siretEtablissementPredecesseur:39860733300042"
    )

    request = api.liens_succession(
        q=(
            criteria.Field("siretEtablissementPredecesseur", "00555008200027")
            & criteria.Field("dateLienSuccession", "2004-04-01")
        ),
    )
    assert (
        request.url
        == BASE_SIRET_URL
        + "/liensSuccession?q=siretEtablissementPredecesseur:00555008200027 AND dateLienSuccession:2004-04-01"
    )


@pytest.mark.vcr()
def test_liens_succession_search_request(api: ApiInsee) -> None:
    request = api.liens_succession(
        q=criteria.Field("siretEtablissementPredecesseur", 39860733300042),
    )
    data = cast(Dict[str, Any], request.get())
    siret_predecesseur = data["liensSuccession"][0]["siretEtablissementPredecesseur"]

    assert siret_predecesseur == "39860733300042"

    request = api.liens_succession(
        q=(
            criteria.Field("siretEtablissementPredecesseur", "00555008200027")
            & criteria.Field("dateLienSuccession", "2004-04-01")
        ),
    )
    data = cast(Dict[str, Any], request.get())
    siret_predecesseur = data["liensSuccession"][0]["siretEtablissementPredecesseur"]
    assert siret_predecesseur == "00555008200027"
    assert data["liensSuccession"][0]["dateLienSuccession"] == "2004-04-01"
