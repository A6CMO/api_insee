class RequestExeption(Exception):
    def __init__(self, request):
        self.request = request

    def badRequest(self):
        self.message = f"bad request url : {self.request.url}"

        return self

    def __str__(self):
        return self.message
