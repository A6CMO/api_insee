class AuthenticationError(Exception):
    pass


class InvalidCredentialsError(AuthenticationError):
    def __init__(self, credential) -> None:
        message = (
            f"Invalid consumer key or secret."
            f" key : {credential.key} secret : {credential.secret}"
        )

        super().__init__(message)
