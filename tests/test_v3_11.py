import pytest

from api_insee import ApiInsee


@pytest.mark.vcr()
def test_siret(api_311: ApiInsee) -> None:
    response = api_311.siret(nombre=0).get()

    assert response["header"]["statut"] == 200  # type: ignore[index]


@pytest.mark.vcr()
def test_siren(api_311: ApiInsee) -> None:
    response = api_311.siren(nombre=0).get()

    assert response["header"]["statut"] == 200  # type: ignore[index]


@pytest.mark.vcr()
def test_liens_succession(api_311: ApiInsee) -> None:
    response = api_311.liens_succession(nombre=0).get()

    assert response["header"]["statut"] == 200  # type: ignore[index]
