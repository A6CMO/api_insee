import time
from typing import Any, Optional


class ClientToken:
    def __init__(self, **data: Any) -> None:
        self.token_type: Optional[str] = data.get("token_type")
        self.epoch_expiration: int = data.get("expires_in", 0) + int(time.time())
        self.access_token: Optional[str] = data.get("access_token")
        self.scope: Optional[str] = data.get("scope")
