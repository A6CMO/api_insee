from typing import Any

from .base import Base


class Range(Base):
    def __init__(self, name: str, left: Any, right: Any, exclude: bool = False) -> None:
        self.name = name
        self.left = left
        self.right = right
        self.exclude = exclude

    def to_url_params(self) -> str:
        return (
            f"{self.name}:{self.left_symbol}{self.left}"
            f" TO {self.right}{self.right_symbol}"
        )

    @property
    def left_symbol(self) -> str:
        return "{" if self.exclude else "["

    @property
    def right_symbol(self) -> str:
        return "}" if self.exclude else "]"
