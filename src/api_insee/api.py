from typing import Any, TypeVar

from api_insee.request.request import RequestService
from api_insee.request.request_entreprises import (
    RequestEntrepriseServiceLiensSuccession,
    RequestEntrepriseServiceSiren,
    RequestEntrepriseServiceSiret,
)
from api_insee.utils.auth_service import AuthService, MockAuth

T = TypeVar("T", bound=RequestService)


class ApiInsee:
    def __init__(self, key, secret, format="json", noauth=False):
        if noauth:
            self.auth = MockAuth()
        else:
            self.auth = AuthService(key=key, secret=secret)
        self.format = format

    def use(self, serviceName, requestService):
        def wrap(*args, **kwargs):
            service = requestService(*args, **kwargs)
            service.format = self.format
            service.useToken(self.auth.token)
            return service

        setattr(self, serviceName, wrap)

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

    def _wrap(
        self,
        request_service: type[T],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        service = request_service(*args, **kwargs)
        service.format = self.format
        service.useToken(self.auth.token)

        return service
