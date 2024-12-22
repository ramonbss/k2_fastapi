from pydantic import BaseModel


class UserCredentials(BaseModel):
    username: str
    password: str


class BaseUser(BaseModel):
    name: str
    email: str
