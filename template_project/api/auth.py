from typing import Any

from fastapi import HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import DecodeError, ExpiredSignatureError

from template_project.config import SecretAPISettings
from template_project.security import decode_jwt_token

secret_api_settings = SecretAPISettings()  # type: ignore


def verify_jwt_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> dict[str, Any]:
    """
    Verify the JSON Web Token (JWT) from the request authorization header.

    Dependency for `FastAPI` endpoints to ensure that a valid JWT Bearer token is
    present in the request.

    Args:
        request: The current HTTP request object, automatically passed in by `FastAPI`.
        credentials: The Bearer token credentials from the request header, provided
            by the `HTTPBearer` security scheme.

    Returns:
        A dictionary representation of the decoded token payload.

    Raises:
        HTTPException: Status code 401 if the token is missing, has an invalid
            'Bearer' prefix, is expired, or is invalid.

    Note:
        - Sets `request.state.payload` to the decoded token payload.
    """
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing 'Bearer' prefix",
        )

    try:
        payload = decode_jwt_token(credentials.credentials)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )

    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    request.state.payload = payload
    return payload


def verify_api_token(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> bool:
    """
    Verify an API token from the request authorization header.

    Dependency for `FastAPI` endpoints to validate that the provided Bearer token matches
    a predefined API token.

    Args:
        credentials: The Bearer token credentials from the request header, provided
            by the `HTTPBearer` security scheme.

    Returns:
        Returns True if the API token is valid.

    Raises:
        HTTPException: Status code 401 if the token is missing, has an invalid
        'Bearer' prefix, or does not match the expected API token.
    """
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing 'Bearer' prefix",
        )

    if credentials.credentials != secret_api_settings.TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token"
        )

    return True
