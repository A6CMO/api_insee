from typing import TYPE_CHECKING, Any, Type, TypeVar, Union

from api_insee.conf import ApiUrls, ApiVersion
from api_insee.request.request_entreprises import (
    RequestEntrepriseServiceLiensSuccession,
    RequestEntrepriseServiceSiren,
    RequestEntrepriseServiceSiret,
)
from api_insee.request.request_informations import RequestInformationsService
from api_insee.request.request_token import RequestTokenService
from api_insee.utils.auth_service import AuthService

if TYPE_CHECKING:
    from api_insee.request.request import AvailableFormat, RequestService
    from api_insee.utils.client_credentials import ClientCredentials

    T = TypeVar("T", bound=RequestService)
else:
    T = None


class ApiInsee:
    api_urls: ApiUrls

    def __init__(  # noqa: PLR0913
        self,
        key: str,
        secret: str,
        format: "AvailableFormat" = "json",
        api_version: ApiVersion = ApiVersion.V_3_11,
        auth_service: Union[Type[AuthService], None] = None,
    ) -> None:
        self.format = format
        self.api_urls = api_version.urls

        auth_service = auth_service or AuthService
        self.auth = auth_service(
            key,
            secret,
            self._request_token_service_factory,
        )

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

    def _request_token_service_factory(
        self,
        credentials: "ClientCredentials",
    ) -> RequestTokenService:
        service = RequestTokenService(credentials)
        service.api_urls = self.api_urls

        return service

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
