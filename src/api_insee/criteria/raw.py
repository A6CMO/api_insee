from .base import Base


class Raw(Base):
    def __init__(self, value):
        self.value = value

    def validate(self):
        return True

    def to_url_params(self):
        return self.value
