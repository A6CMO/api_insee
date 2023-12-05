from typing import Any, Type, TypeVar

from api_insee.conf import ApiUrls, ApiVersion
from api_insee.request.request import AvailableFormat, RequestService
from api_insee.request.request_entreprises import (
    RequestEntrepriseServiceLiensSuccession,
    RequestEntrepriseServiceSiren,
    RequestEntrepriseServiceSiret,
)
from api_insee.request.request_informations import RequestInformationsService
from api_insee.request.request_token import RequestTokenService
from api_insee.utils.auth_service import AuthService
from api_insee.utils.client_credentials import ClientCredentials

T = TypeVar("T", bound=RequestService)


class ApiInsee:
    api_urls: ApiUrls

    def __init__(
        self,
        key: str,
        secret: str,
        format: AvailableFormat = "json",
        api_version: ApiVersion = ApiVersion.V_3,
    ) -> None:
        self.format = format
        self.api_urls = api_version.urls
        self.auth = self._get_auth_service(key, secret)

    def siret(self, *args: Any, **kwargs: Any) -> RequestEntrepriseServiceSiret:
        return self._wrap(RequestEntrepriseServiceSiret, *args, **kwargs)

    def siren(self, *args: Any, **kwargs: Any) -> RequestEntrepriseServiceSiren:
        return self._wrap(RequestEntrepriseServiceSiren, *args, **kwargs)

    def informations(self, *args: Any, **kwargs: Any) -> RequestInformationsService:
        return self._wrap(RequestInformationsService, *args, **kwargs)

    def liens_succession(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> RequestEntrepriseServiceLiensSuccession:
        return self._wrap(RequestEntrepriseServiceLiensSuccession, *args, **kwargs)

    def _get_auth_service(self, key: str, secret: str) -> AuthService:
        def factory(credentials: ClientCredentials) -> RequestTokenService:
            service = RequestTokenService(credentials)
            service.api_urls = self.api_urls

            return service

        return AuthService(key, secret, factory)

    def _wrap(
        self,
        request_service: Type[T],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        service = request_service(*args, **kwargs)
        service.format = self.format
        service.use_token(self.auth.token)
        service.api_urls = self.api_urls

        return service
