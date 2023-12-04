from .base import Base


class Raw(Base):
    def __init__(self, value: str) -> None:
        self.value = value

    def validate(self) -> bool:
        return True

    def to_url_params(self) -> str:
        return self.value
