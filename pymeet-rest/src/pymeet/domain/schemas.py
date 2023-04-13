"""Schemas

Represents the schemas for transferring data in or out pymeet application.
"""
import datetime
from typing import Any, TypeVar

from pydantic import BaseModel, BaseConfig, Field, validator, EmailStr

from pymeet.app import formatters

PASSWORD_MIN_LENGTH = 8

T = TypeVar("T", bound="CamelCaseModel")


class CamelCaseModel(BaseModel):
    """
    A base which attributes can be translated to camel case.
    """

    def dict(self, *args, **kwargs) -> dict[str, Any]:

        try:
            kwargs.pop('exclude_none')
        except KeyError:
            pass

        return super().dict(*args, exclude_none=True, **kwargs)

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
    data: BaseUser | list[BaseUser] = Field(title="User", description="User data output without sensible information")


class MeetingOptionBase(CamelCaseModel):
    """
    Represents a meeting option.
    """

    date: datetime.date = Field(title="Date", description="The date of the option.")
    hour: int = Field(title="Hour", description="The hour of the option.", ge=0, le=23)


class MeetingOptionIn(MeetingOptionBase):
    """
    Represents a meeting option.
    """
    pass


class MeetingOptionOut(MeetingOptionBase):
    """
    Represents a meeting option.
    """

    votes: list[BaseUser] = Field(title="Votes", description="Who voted the option.")


class MeetingEventBase(CamelCaseModel):
    """
    Represents a meeting event.
    """

    name: str = Field(title="Title", description="The title of the event.")
    attendees: set[BaseUser] = Field(title="Attendees", description="The attendees of the event.")
    options: list[MeetingOptionBase] = Field(title="Options", description="The options for the event.")


class MeetingEventOut(MeetingEventBase):
    """
    Represents a meeting event.
    """
    options: list[MeetingOptionOut] = Field(title="Options", description="The options for the event.")
    voted_date: datetime.datetime | None = Field(title="Voted Date",
                                                 description="The date when the event was voted.",
                                                 default=None)


class MeetingEventIn(MeetingEventBase):
    """
    Represents a meeting event input.
    """

    organizer: str = Field(title="Organizer", description="The organizer of the event.")
    attendees: set[str] | None = Field(title="Attendees", description="The attendees of the event.")
    options: list[MeetingOptionIn] = Field(title="Options", description="The options for the event.")


class MeetingResponse(CamelCaseModel):
    """
    Represents a meeting event.
    """
    data: MeetingEventBase | list[MeetingEventBase] = Field(title="Meeting", description="Meeting data output")
