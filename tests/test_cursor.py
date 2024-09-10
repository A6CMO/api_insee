import pytest

from api_insee import ApiInsee, criteria

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"


@pytest.mark.vcr
def test_request_first_pages(api: ApiInsee) -> None:
    request = api.siren(criteria.Raw("*"))

    pages = request.pages()
    first = next(pages)

    assert first["header"]["statut"] == 200
    assert first["header"]["curseur"] == "*"
    assert first["header"]["curseurSuivant"]


@pytest.mark.vcr
def test_request_iterate_on_pages(api: ApiInsee) -> None:
    request = api.siren(criteria.Raw("*"))

    cursors = []

    for page in request.pages():
        cursors.append(page["header"]["curseur"])
        if len(cursors) > 2:
            break

    assert cursors[0] != cursors[1]
    assert cursors[1] != cursors[2]
