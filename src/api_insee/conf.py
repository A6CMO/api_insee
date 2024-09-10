from enum import Enum
from typing import Literal, TypedDict

_BASE_URL = "https://api.insee.fr"
_TOKEN_URL = f"{_BASE_URL}/token"


ApiPathName = Literal[
    "path_token",
    "path_siren",
    "path_siret",
    "path_informations",
    "path_liens_succession",
]


class ApiUrls(TypedDict):
    path_token: str
    path_siren: str
    path_siret: str
    path_informations: str
    path_liens_succession: str


class ApiVersion(Enum):
    V_3_11 = f"{_BASE_URL}/api-sirene/3.11"

    @property
    def urls(self) -> ApiUrls:
        return {
            "path_token": _TOKEN_URL,
            "path_siren": f"{self.value}/siren",
            "path_siret": f"{self.value}/siret",
            "path_informations": f"{self.value}/informations",
            "path_liens_succession": f"{self.value}/siret/liensSuccession",
        }
