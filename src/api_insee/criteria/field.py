from .base import Base


class Field(Base):
    def __init__(self, name, value, *args, **kwargs):
        self.name = name
        self.value = value

    def to_url_params(self):
        query = self.representation

        if self.negative:
            query = "-" + query

        return query

    @property
    def representation(self):
        return f"{self.name}:{self.value}"
