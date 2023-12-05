from pathlib import Path
from typing import Dict, Final
from unittest.mock import MagicMock

from api_insee import ApiInsee
from api_insee.utils.auth_service import AuthService

PROJECT_ROOT: Final = Path(__file__).parent.parent


def parse_env_file() -> Dict[str, str]:
    with Path(PROJECT_ROOT, ".env").open() as file:
        lines = (
            line.split("=")
            for line in file.read().splitlines(keepends=False)
            if line and not line.startswith("#")
        )

        return {key.strip(): value.strip() for key, value in lines}


class ApiInseeTestDouble(ApiInsee):
    def _get_auth_service(self, key: str, secret: str) -> AuthService:  # noqa: ARG002
        return MagicMock()
