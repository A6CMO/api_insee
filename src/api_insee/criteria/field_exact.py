from .field import Field


class FieldExact(Field):
    @property
    def representation(self):
        return f'{self.name}:"{self.value}"'
