from .base import Base


class Periodic(Base):
    def __init__(self, *criteria, operator="AND", **kwargs):
        self.criteria_list = criteria
        self.operator = operator

    def to_url_params(self):
        fields = (" " + self.operator + " ").join(
            [ct.to_url_params() for ct in self.criteria_list]
        )
        return f"periode({fields})"
