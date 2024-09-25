import uuid
from datetime import datetime

from sqlmodel import Field, func

from template_project.models.validation import UserBase


class User(UserBase, table=True):
    """
    Database model representing a user.

    Inherits attributes from `UserBase`:
        email (EmailStr): The email address of the user, which is unique and indexed.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.

    Attributes:
        id (UUID): The unique identifier of the user.
        hashed_password (str): The hashed version of the user's password.
        created_at (datetime): The timestamp when the user was created, assigned by the database.
        updated_at (datetime): The timestamp when the user was last updated, assigned by the database on update.

    Notes:
        The `created_at` and `updated_at` fields have a default value set by the database, using `server_default`.
        Additionally `updated_at` is updated automatically on modification.
    """

    __tablename__ = "users"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default=None,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
