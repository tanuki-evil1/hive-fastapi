from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends

from app.api.dependencies import get_auth_service
from app.config import settings
from app.domain.models.token import Token, RefreshTokenIn
from app.domain.models.user import UserLoginSchema
from app.domain.services.auth import AuthService
from app.infrastructure.security.jwt import create_access_token, create_refresh_token, decode_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token")
async def login_for_access_token(
        form_data: UserLoginSchema,
        auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)
    return Token.model_validate({"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})


@auth_router.post("/refresh")
async def refresh_access_token(refresh_data: RefreshTokenIn) -> Token:
    try:
        payload = decode_token(refresh_data.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Недействительный refresh токен")
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Недействительный refresh токен")
    except Exception:
        raise HTTPException(status_code=401, detail="Недействительный refresh токен")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    new_access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    new_refresh_token = create_refresh_token(data={"sub": username}, expires_delta=refresh_token_expires)

    return Token.model_validate({
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    })
