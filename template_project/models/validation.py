import uuid

from pydantic import EmailStr
from sqlmodel import AutoString, Field, SQLModel


class UserBase(SQLModel):
    """
    Base model for user data.

    Attributes:
        email (EmailStr): The email address of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """

    email: EmailStr = Field(unique=True, index=True, max_length=255, sa_type=AutoString)
    first_name: str
    last_name: str


class UserUpdate(SQLModel):
    """
    Model for updating user data.

    Attributes:
        first_name (str | None): The first name of the user (optional).
        last_name (str | None): The last name of the user (optional).
    """

    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)


class UserCreate(UserBase):
    """
    Model for creating a new user.

    Inherits attributes from `UserBase`:
        email (EmailStr): The email address of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.

    Attributes:
        password (str): The password for the user, which must be between 8 and 40 characters.
    """

    password: str = Field(min_length=8, max_length=40)


class UserLogin(SQLModel):
    """
    Model for user login data.

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The password for the user, which must be between 8 and 40 characters.
    """

    email: EmailStr
    password: str = Field(min_length=8, max_length=40)


class UserPublic(UserBase):
    """
    Response model containing the user's public information.

    Inherits attributes from `UserBase`:
        email (EmailStr): The email address of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.

    Attributes:
        id (UUID): The unique identifier of the user.
    """

    id: uuid.UUID


class TokenResponse(SQLModel):
    """
    Response model containing the access token.

    Attributes:
        access_token (str): The JWT access token issued for the user.
    """

    access_token: str
