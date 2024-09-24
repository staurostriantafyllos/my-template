from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from template_project.config import SecretTokenSettings, TokenSettings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

secret_token_settings = SecretTokenSettings()  # type: ignore
token_settings = TokenSettings()  # type: ignore


def create_access_token(
    subject: str | Any,
    extra_options: dict = {},
) -> str:
    """
    Create an encoded JSON Web Token (JWT) for authentication.

    Generate an access token containing the subject and optional additional
    claims. The token is encoded using the secret key, algorithm and expiration time
    found in the environment which are loaded using the `SecretTokenSettings` and
    `TokenSettings` models.

    Args:
        subject: The user identifier for whom the token is being created.
        extra_options (optional): Additional claims to include in the token. Defaults to an empty dictionary.

    Returns:
        String representation of the encoded JSON Web Token (JWT).
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=token_settings.EXPIRATION_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    to_encode.update(extra_options)
    encoded_jwt = jwt.encode(
        to_encode,
        secret_token_settings.SECRET_KEY,
        algorithm=token_settings.ALGORITHM,
    )
    return encoded_jwt


def decode_jwt_token(token: str) -> dict[str, Any]:
    """
    Decode a JSON Web Token (JWT) and verify its validity.

    Decode the JWT and verify its signature and expiration. The token is decoded using
    the settings found in the environment, which are loaded using the `SecretTokenSettings`
    and `TokenSettings` models.

    Args:
        token: The encoded JWT to decode.

    Returns:
        A dictionary representation of the decoded token payload.
    """
    return jwt.decode(
        token,
        key=secret_token_settings.SECRET_KEY,
        algorithms=[token_settings.ALGORITHM],
        options={"verify_exp": token_settings.VERIFY_EXPIRATION},
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain text password."""
    return pwd_context.hash(password)
