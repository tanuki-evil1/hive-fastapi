from datetime import datetime, timedelta, UTC
from typing import Optional
import jwt
from app.config import settings


def create_access_token(username: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def create_refresh_token(username: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


async def refresh_access_token(self, refresh_token: str) -> Optional[str]:
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if not username:
            return None
        return self.create_access_token(username)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
