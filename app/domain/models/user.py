from pydantic import BaseModel


class UserAddSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserSchema(UserAddSchema):
    id: int
