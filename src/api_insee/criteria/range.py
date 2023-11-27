from .base import Base


class Range(Base):
    name = None
    left = None
    right = None
    exclude = False

    def __init__(self, name, left, right, exclude=False):
        self.name = name
        self.left = left
        self.right = right
        self.exclude = exclude

    def to_url_params(self):
        return (
            f"{self.name}:{self.left_symbol}{self.left}"
            f" TO {self.right}{self.right_symbol}"
        )

    @property
    def left_symbol(self):
        return "{" if self.exclude else "["

    @property
    def right_symbol(self):
        return "}" if self.exclude else "]"
