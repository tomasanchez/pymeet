"""Schemas

Represents the schemas for transferring data in or out pymeet application.
"""
from pydantic import BaseModel, BaseConfig, Field, validator, EmailStr

from pymeet.app import formatters

PASSWORD_MIN_LENGTH = 8


class CamelCaseModel(BaseModel):
    """
    A base which attributes can be translated to camel case.
    """

    class Config(BaseConfig):
        alias_generator = formatters.to_camel
        allow_population_by_field_name = True


class BaseUser(CamelCaseModel):
    """
    Base User attributes.
    """

    username: str = Field(title="Username", description="The username of the user.")
    email: EmailStr = Field(title="Email", description="The email of the user")

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v


class UserIn(BaseUser):
    """
    Represents a user.
    """

    password1: str = Field(title="Password",
                           description="The password of the user.",
                           min_length=PASSWORD_MIN_LENGTH)
    password2: str = Field(title="Repeat Password",
                           description="Check for password.",
                           min_length=PASSWORD_MIN_LENGTH)

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v


class UserResponse(CamelCaseModel):
    """
    Represents a user.
    """
    data: BaseUser = Field(title="User", description="User data output without sensible information")
