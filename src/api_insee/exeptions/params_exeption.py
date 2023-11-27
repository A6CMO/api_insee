class ParamsExeption(Exception):
    name = None
    value = None

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def wrongFormat(self, paramFormat):
        self.message = (
            f"Wrong format for {self.name}: {self.value}. Excepted format {paramFormat}"
        )

        return self

    def __str__(self):
        return self.message
