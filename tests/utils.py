from pathlib import Path
from typing import Final

PROJECT_ROOT: Final = Path(__file__).parent.parent


def parse_env_file() -> dict[str, str]:
    with Path(PROJECT_ROOT, ".env").open() as file:
        lines = (
            line.split("=")
            for line in file.read().splitlines(keepends=False)
            if line and not line.startswith("#")
        )

        return {key.strip(): value.strip() for key, value in lines}
