from pydantic import BaseModel, ConfigDict


class RefreshTokenIn(BaseModel):
    refresh_token: str


class Token(RefreshTokenIn):
    access_token: str
    token_type: str
