import pydantic
from typing import Optional, Type


class CreateUser(pydantic.BaseModel):
    username: str
    password: str
    email: str

    @pydantic.validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('password is too short')
        return value


class PatchUser(pydantic.BaseModel):
    username: Optional[str]
    password: Optional[str]

    @pydantic.validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('password is too short')
        return value


class CreateNews(pydantic.BaseModel):
    title: str
    content: str

    @pydantic.validator('title')
    def validate_password(cls, value):
        if len(value) < 3:
            raise ValueError('title is too short')
        return value


class PatchNews(pydantic.BaseModel):
    title: Optional[str]
    content: Optional[str]

    @pydantic.validator('title')
    def validate_password(cls, value):
        if len(value) < 3:
            raise ValueError('title is too short')
        return value


VALIDATION_CLASS = Type[CreateUser] | Type[PatchUser] | Type[CreateNews] | Type[PatchNews]
