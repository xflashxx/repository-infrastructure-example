import secrets
from typing import Final, Never

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from repository_infrastructure_example.application.api.dependencies import (
    get_application_context,
)
from repository_infrastructure_example.application.context import ApplicationContext

_API_KEY_HEADER_NAME: Final[str] = "X-API-KEY"

_api_key_header: APIKeyHeader = APIKeyHeader(
    name=_API_KEY_HEADER_NAME, auto_error=False
)


def raise_unauthorized_exception() -> Never:
    """
    Raises an HTTP 401 Unauthorized exception for API key authentication.
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
        headers={"WWW-Authenticate": "API Key"},
    )


def verify_endpoint_access(
    *,
    provided: str | None = Security(_api_key_header),
    context: ApplicationContext = Depends(get_application_context),
) -> None:
    """
    Verify endpoint access using API key authentication.

    :param provided: The API key provided in the request header.
    :param context: The application context.
    :return: None if authentication is successful.
    :raises HTTPException: If authentication fails.
    """

    require_authentication: bool = context.settings.api.require_authentication

    # Authentication disabled: always allow
    if not require_authentication:
        return

    # Authentication enabled: key must be present
    if provided is None:
        raise_unauthorized_exception()

    # If the expected API key is not set, raise an error
    # (should never be the case due to settings validation)
    expected = context.settings.api.api_key
    if expected is None:
        raise_unauthorized_exception()

    # Compare provided key with expected key
    if not secrets.compare_digest(provided, expected.get_secret_value()):
        raise_unauthorized_exception()
