from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth_service import AuthService
from app.dependencies import get_auth_service

router = APIRouter()


@router.post("/login")
async def login(username: str, password: str, auth_service: AuthService = Depends(get_auth_service)):
    token_data = await auth_service.authenticate_user(username, password)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return token_data


@router.post("/refresh")
async def refresh_token(refresh_token: str, auth_service: AuthService = Depends(get_auth_service)):
    new_token = await auth_service.refresh_access_token(refresh_token)
    if not new_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    return new_token