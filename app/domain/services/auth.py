from typing import Optional

from app.infrastructure.ad.ad_client import ADClient
from app.infrastructure.security.jwt import create_access_token, create_refresh_token


class AuthService:
    def __init__(self, ad_client: ADClient):
        self.ad_client = ad_client

    async def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        if await self.ad_client.authenticate(username, password):
            access_token = create_access_token(username)
            refresh_token = create_refresh_token(username)
            return {"access_token": access_token, "refresh_token": refresh_token}
        return None
