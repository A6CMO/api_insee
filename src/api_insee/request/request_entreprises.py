from typing import Any, Iterator, Optional, Union, cast

from api_insee.conf import API_VERSION
from api_insee.exeptions.request_error import RequestError
from .request import AvailableFormat, AvailableMethod, RequestService


class RequestEntrepriseService(RequestService):
    path = ""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        champs = kwargs.get("champs")
        if champs and isinstance(champs, list):
            kwargs.update({"champs": ",".join(champs)})

        self.reference: Optional[str] = None
        if args and isinstance(args[0], str):
            self.reference = args[0]
            args = args[1:]

        super(RequestEntrepriseService, self).__init__(*args, **kwargs)

    def get(  # type: ignore[override]
        self,
        format: Optional[AvailableFormat] = None,
        method: Optional[AvailableMethod] = None,
    ) -> Union[str, dict[str, Any]]:
        if self._url_params.get("q", False) and not method:
            method = "post"
        else:
            method = method or "get"

        return super(RequestEntrepriseService, self).get(format=format, method=method)

    @property
    def url_path(self) -> str:
        reference = f"/{self.reference}" if self.reference else ""

        return f'{API_VERSION["url"]}{self.path}{reference}'

    def pages(self, nombre: int = 100) -> Iterator[dict[str, Any]]:
        if self.format == "csv":
            raise RequestError("You cannot use csv format with cursor")

        cursor = ""
        next_cursor = "*"

        nombre = self._url_params.get("nombre", nombre)  # type: ignore[assignment]
        self.set_url_params("nombre", nombre)

        while cursor != next_cursor:
            self.set_url_params("curseur", next_cursor)

            # Pagination is not available with csv format, we can cast response
            # as dict.
            page = cast(dict[str, Any], self.get(method="get"))

            yield page

            cursor = page["header"]["curseur"]
            next_cursor = page["header"]["curseurSuivant"]


class RequestEntrepriseServiceSiren(RequestEntrepriseService):
    path = API_VERSION["path_siren"]

    def __init__(self, *args, **kwargs) -> None:
        if len(args) and isinstance(args[0], list):
            kwargs.update({"q": " OR ".join(["siren:" + siren for siren in args[0]])})

        super(RequestEntrepriseServiceSiren, self).__init__(*args, **kwargs)


class RequestEntrepriseServiceSiret(RequestEntrepriseService):
    path = API_VERSION["path_siret"]

    def __init__(self, *args, **kwargs) -> None:
        if len(args) and isinstance(args[0], list):
            kwargs.update({"q": " OR ".join(["siret:" + siret for siret in args[0]])})

        super(RequestEntrepriseServiceSiret, self).__init__(*args, **kwargs)


class RequestEntrepriseServiceLiensSuccession(RequestEntrepriseService):
    path = API_VERSION["path_liens_succession"]

    def __init__(self, *args, **kwargs) -> None:
        super(RequestEntrepriseServiceLiensSuccession, self).__init__(*args, **kwargs)

    def get(  # type: ignore[override]
        self,
        format: Optional[AvailableFormat] = None,
        method: Optional[AvailableMethod] = "get",
    ) -> Union[str, dict[str, Any]]:
        return super(RequestEntrepriseService, self).get(format=format, method=method)
