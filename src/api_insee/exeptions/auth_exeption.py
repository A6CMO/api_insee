class AuthExeption(Exception):
    credential = None

    def __init__(self, credential):
        self.key = credential.key
        self.secret = credential.secret
        self.message: str | None = None

    def invalidkeyAndSecret(self):
        self.message = (
            f"Invalid consumer key or secret. key : {self.key} secret : {self.secret}"
        )

        return self

    def unauthorized(self, reason=False):
        self.message = (
            f"Api connection unauthorized. key: {self.key} secret: {self.secret}"
        )

        if reason:
            self.message += f"\n {reason}"

        return self

    def __str__(self):
        return self.message
