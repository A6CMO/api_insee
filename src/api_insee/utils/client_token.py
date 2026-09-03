from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, TypeAlias

if TYPE_CHECKING:
    from api_insee.utils.api_key import ApiKey


class _PropertyTokenProvider(Protocol):
    @property
    def access_token(self) -> "ApiKey": ...


class _FieldTokenProvider(Protocol):
    access_token: "ApiKey"


TokenProvider: TypeAlias = _FieldTokenProvider | _PropertyTokenProvider


@dataclass
class ClientToken:
    access_token: "ApiKey"
