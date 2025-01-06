from typing import TYPE_CHECKING, Any, TypeVar

from api_insee.conf import ApiUrls, ApiVersion
from api_insee.request.request_entreprises import (
    RequestEntrepriseServiceLiensSuccession,
    RequestEntrepriseServiceSiren,
    RequestEntrepriseServiceSiret,
)
from api_insee.request.request_informations import RequestInformationsService
from api_insee.utils.api_key import ApiKey
from api_insee.utils.client_token import ClientToken

if TYPE_CHECKING:
    from api_insee.request.request import AvailableFormat, RequestService

    T = TypeVar("T", bound=RequestService)
else:
    T = None


class ApiInsee:
    api_urls: ApiUrls

    def __init__(
        self,
        api_key: str,
        format: "AvailableFormat" = "json",
        api_version: ApiVersion = ApiVersion.V_3_11,
    ) -> None:
        self.format = format
        self.api_urls = api_version.urls
        self.api_key = ApiKey(api_key)

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

    def _wrap(
        self,
        request_service: type[T],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        service = request_service(*args, **kwargs)
        service.format = self.format
        service.use_token(ClientToken(access_token=self.api_key))
        service.api_urls = self.api_urls

        return service
