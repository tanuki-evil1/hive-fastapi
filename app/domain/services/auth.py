from passlib.context import CryptContext

from app.infrastructure.ad.ad_client import ADClient
from app.infrastructure.db.repositories.user import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str):
        ad_client = ADClient(username=username, password=password)
        if ad_client.authenticate():
            return ad_client.get_user_data()
        return None
