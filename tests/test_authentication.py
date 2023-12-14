import pytest

from api_insee import ApiInsee
from api_insee.utils.auth_service import AuthService, RequestTokenServiceFactory

from tests.conftest import SIRENE_API_CONSUMER_KEY, SIRENE_API_CONSUMER_SECRET

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

from api_insee.exceptions.authentication_error import InvalidCredentialsError


def test_missing_credentials() -> None:
    with pytest.raises(InvalidCredentialsError):
        ApiInsee("", "")


@pytest.mark.vcr()
def test_unauthorized_credentials() -> None:
    with pytest.raises(InvalidCredentialsError):
        ApiInsee(
            key="wrong api key",
            secret=SIRENE_API_CONSUMER_SECRET,
        )


@pytest.mark.vcr()
def test_generate_token() -> None:
    api = ApiInsee(
        key=SIRENE_API_CONSUMER_KEY,
        secret=SIRENE_API_CONSUMER_SECRET,
    )

    assert api.auth.token.access_token


def test_use_custom_auth_service() -> None:
    class CustomAuthService(AuthService):
        def __init__(
            self,
            key: str,
            secret: str,
            request_token_service_factory: RequestTokenServiceFactory,
        ) -> None:
            raise NotImplementedError

    with pytest.raises(NotImplementedError):
        ApiInsee("foo", "bar", auth_service=CustomAuthService)
