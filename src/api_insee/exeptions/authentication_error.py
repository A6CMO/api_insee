from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api_insee.utils.client_credentials import ClientCredentials


class AuthenticationError(Exception):
    pass


class InvalidCredentialsError(AuthenticationError):
    def __init__(self, credential: "ClientCredentials") -> None:
        message = (
            f"Invalid consumer key or secret."
            f" key : {credential.key} secret : {credential.secret}"
        )

        super().__init__(message)
