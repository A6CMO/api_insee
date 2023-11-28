from typing import Any

from .base import Base


class Field(Base):
    def __init__(self, name: str, value: Any) -> None:
        self.name = name
        self.value = value

    def to_url_params(self) -> str:
        minus = "-" if self.negative else ""

        return f"{minus}{self.representation}"

    @property
    def representation(self) -> str:
        return f"{self.name}:{self.value}"
