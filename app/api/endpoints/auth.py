from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends

from app.config import settings
from app.infrastructure.security.jwt import create_access_token, create_refresh_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])
protected_router = APIRouter(prefix="/users", tags=["users"])


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: UserIn,
        auth_service: AuthService = Depends(get_auth_service)
):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@auth_router.post("/refresh", response_model=Token)
async def refresh_access_token(
        refresh_data: RefreshTokenIn
):
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

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}


@protected_router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserOut(id=current_user.id, username=current_user.username)
