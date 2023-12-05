from typing import Any, Type, TypeVar

from api_insee.request.request import AvailableFormat, RequestService
from api_insee.request.request_entreprises import (
    RequestEntrepriseServiceLiensSuccession,
    RequestEntrepriseServiceSiren,
    RequestEntrepriseServiceSiret,
)
from api_insee.utils.auth_service import AuthService

T = TypeVar("T", bound=RequestService)


class ApiInsee:
    def __init__(
        self,
        key: str,
        secret: str,
        format: AvailableFormat = "json",
    ) -> None:
        self.format = format
        self.auth = self._get_auth_service(key, secret)

    def siret(self, *args: Any, **kwargs: Any) -> RequestEntrepriseServiceSiret:
        return self._wrap(RequestEntrepriseServiceSiret, *args, **kwargs)

    def siren(self, *args: Any, **kwargs: Any) -> RequestEntrepriseServiceSiren:
        return self._wrap(RequestEntrepriseServiceSiren, *args, **kwargs)

    def liens_succession(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> RequestEntrepriseServiceLiensSuccession:
        return self._wrap(RequestEntrepriseServiceLiensSuccession, *args, **kwargs)

    def _get_auth_service(self, key: str, secret: str) -> AuthService:
        return AuthService(key=key, secret=secret)

    def _wrap(
        self,
        request_service: Type[T],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        service = request_service(*args, **kwargs)
        service.format = self.format
        service.use_token(self.auth.token)

        return service
