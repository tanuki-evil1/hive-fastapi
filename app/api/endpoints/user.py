from fastapi import APIRouter

from app.domain.services.user import UserService

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("")
async def get_users_data():
    """Получение полей пользователя."""
    user_service = UserService('v.rin', 'oMaY6oor')
    return user_service.get_user_data()


@router.post("/login")
async def login():
    pass


@router.post("/logout")
async def logout():
    pass