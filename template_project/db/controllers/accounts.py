import uuid

from sqlmodel import Session, select

from template_project.models.database import User
from template_project.models.validation import UserCreate, UserUpdate
from template_project.security import get_password_hash, verify_password


def get_user_by_email(session: Session, email: str) -> User | None:
    """Retrieve a user by email address."""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def get_user_by_id(session: Session, user_id: uuid.UUID) -> User | None:
    """Retrieve a user by ID."""
    return session.get(User, user_id)


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    """
    Authenticate a user using their email and password.

    Check if a user exists with the provided email, and verify the given password
    against the stored hashed password.

    Args:
        session: The database session for executing the query.
        email: The email address of the user to authenticate.
        password: The plain text password to verify.

    Returns:
        The user object if successful, or None if authentication fails or the user is not found.
    """
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_user(session: Session, user_in: UserCreate) -> User:
    """
    Create a new user entry in the database.

    Validate the input data, hash the password, and add the new user to the database.
    Return the created user object after flushing the session.

    Args:
        session: The database session for executing the operation.
        user_in: The data for creating the new user, containing the user's email, first name,
            last name and password.

    Returns:
        The newly created user object.
    """
    user = User.model_validate(
        user_in, update={"hashed_password": get_password_hash(user_in.password)}
    )

    session.add(user)
    session.flush()
    session.refresh(user)

    return user


def update_user(
    session: Session, user_in: UserUpdate, user_id: uuid.UUID
) -> User | None:
    """
    Update an existing user's information.

    Fetch the user from the database using the provided user ID, update their details
    with the provided input, and save the changes.

    Args:
        session: The database session for executing the operation.
        user_in: The data for updating the user's information, containing the user's first and last name.
        user_id: The unique identifier of the user to update.

    Returns:
        The updated user object, or None if the user is not found.
    """
    db_user = session.get(User, user_id)

    if not db_user:
        return None

    user_data = user_in.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)

    session.add(db_user)
    session.flush()
    session.refresh(db_user)

    return db_user
