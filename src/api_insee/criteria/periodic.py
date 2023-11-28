from .base import Base, LogicOperator


class Periodic(Base):
    def __init__(self, *criteria: Base, operator: LogicOperator = "AND") -> None:
        self.criteria_list = criteria
        self.operator = operator

    def to_url_params(self) -> str:
        fields = f" {self.operator} ".join(
            ct.to_url_params() for ct in self.criteria_list
        )

        return f"periode({fields})"
