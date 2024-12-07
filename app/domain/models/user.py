from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserAddSchema(UserLoginSchema):
    first_name: str
    last_name: str
    email: str


class UserSchema(UserAddSchema):
    id: int
