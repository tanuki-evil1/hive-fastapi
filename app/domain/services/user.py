from pydantic import EmailStr

from app.infrastructure.ad.ad_client import ADClient

class UserService:
    def __init__(self, username: str, password: str):
        self.ad_client = ADClient(username, password)

    def get_user_data(self):
        return self.ad_client.get_user_data()

    def update_user_data(self, username, data):
        return self.ad_client.update_user_data(username, data)