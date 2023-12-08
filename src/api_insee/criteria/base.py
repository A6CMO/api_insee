from abc import ABC, abstractmethod
from typing import Literal

LogicOperator = Literal["AND", "OR"]


class Base(ABC):
    negative = False

    @abstractmethod
    def to_url_params(self) -> str:
        ...

    def __str__(self) -> str:
        return self.to_url_params()

    def __neg__(self) -> "Base":
        self.negative = not self.negative

        return self

    def __and__(self, criteria: "Base") -> "TreeCriteria":
        return TreeCriteria(self, "AND", criteria)

    def __or__(self, criteria: "Base") -> "TreeCriteria":
        return TreeCriteria(self, "OR", criteria)


class TreeCriteria(Base):
    def __init__(
        self,
        left: Base,
        operator: LogicOperator,
        right: Base,
    ) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def to_url_params(self) -> str:
        return f"{self.left} {self.operator} {self.right}"
