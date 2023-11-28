from .field import Field


class FieldExact(Field):
    @property
    def representation(self) -> str:
        return f'{self.name}:"{self.value}"'
