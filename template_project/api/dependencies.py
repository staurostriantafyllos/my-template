from fastapi import Depends

from template_project.api.auth import verify_jwt_token
from template_project.db.factories import get_db_session


def get_session():
    """
    Provide a database session for use in `FastAPI` endpoints.

    Intended for use with `FastAPI`'s dependency injection system to provide a database
    session where authentication is not required.

    Yields:
        A `SQLModel` session object for interacting with the database.
    """
    yield from get_db_session()


def get_session_by_user(payload: dict = Depends(verify_jwt_token)):
    """
    Provide a database session for use in `FastAPI` endpoints.

    Intended for use with `FastAPI`'s dependency injection system to provide a database
    session where authentication is required.

    Args:
        payload: Utilizes `FastAPI`'s dependency injection to ensure that a valid JWT
            is present in the request.

    Yields:
        A `SQLModel` session object for interacting with the database.
    """
    yield from get_db_session()
