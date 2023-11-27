class Base:
    format_description = " "
    negative = False

    def __init__(self, *args, **kwargs):
        pass

    def validate(self):
        return True

    def toURLParams(self):
        return ""

    def __str__(self) -> str:
        return self.toURLParams()

    def __neg__(self):
        self.negative = not self.negative
        return self

    def __and__(self, criteria):
        return TreeCriteria(self, "AND", criteria)

    def __or__(self, criteria):
        return TreeCriteria(self, "OR", criteria)


class TreeCriteria(Base):
    left = None
    operator = None
    right = None

    def __init__(self, left, operator, right, **kwargs):
        self.left = left
        self.operator = operator
        self.right = right

    def toURLParams(self):
        return f"{self.left} {self.operator} {self.right}"
