from .base import Base


class List(Base):
    def __init__(self, *criteria: Base) -> None:
        self.criteria_list = criteria

    def to_url_params(self) -> str:
        return " AND ".join([ct.to_url_params() for ct in self.criteria_list])
