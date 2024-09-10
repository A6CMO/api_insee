from dataclasses import dataclass, field
from time import time
from typing import Protocol, Union


class _PropertyTokenProvider(Protocol):
    @property
    def token_type(self) -> str: ...

    @property
    def epoch_expiration(self) -> int: ...

    @property
    def access_token(self) -> str: ...

    @property
    def scope(self) -> str: ...


class _FieldTokenProvider(Protocol):
    token_type: str
    epoch_expiration: int
    access_token: str
    scope: str


TokenProvider = Union[_FieldTokenProvider, _PropertyTokenProvider]


@dataclass
class ClientToken:
    token_type: str
    expires_in: int
    access_token: str
    scope: str

    epoch_expiration: int = field(init=False)

    def __post_init__(self) -> None:
        self.epoch_expiration = self.expires_in + int(time())
