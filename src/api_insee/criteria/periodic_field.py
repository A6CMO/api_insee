from .field import Field


class PeriodicField(Field):
    @property
    def representation(self) -> str:
        rp = super(PeriodicField, self).representation

        return f"periode({rp})"
