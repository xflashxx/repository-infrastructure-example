import secrets
from typing import Never

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from repository_infrastructure_example.application.api.dependencies import (
    get_application_context,
)
from repository_infrastructure_example.application.context import ApplicationContext

_http_basic = HTTPBasic(auto_error=False)


def raise_unauthorized_exception() -> Never:
    """
    Raises an HTTP 401 Unauthorized exception for documentation access.
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid documentation credentials",
        headers={"WWW-Authenticate": "Basic"},
    )


def verify_documentation_access(
    credentials: HTTPBasicCredentials | None = Depends(_http_basic),
    context: ApplicationContext = Depends(get_application_context),
) -> None:
    """
    Verify documentation access using HTTP Basic authentication.

    :param credentials: The HTTP Basic credentials provided in the request.
    :param context: The application context.
    :return: None if authentication is successful or not required.
    :raises HTTPException: If authentication is required but fails.
    """
    # If authentication is not required, allow access
    if not context.settings.api.require_authentication:
        return

    # Authentication is required from this point on
    expected_username = context.settings.api.documentation_username
    expected_password = context.settings.api.documentation_password

    # If credentials weren't provided, prompt for them
    if credentials is None:
        raise_unauthorized_exception()

    # If either expected username or password is not set, raise an error
    # (should never be the case due to settings validation)
    if expected_username is None or expected_password is None:
        raise_unauthorized_exception()

    # Compare provided credentials with expected credentials
    is_username_valid: bool = secrets.compare_digest(
        credentials.username,
        expected_username,
    )
    is_password_valid: bool = secrets.compare_digest(
        credentials.password,
        expected_password.get_secret_value(),
    )

    if not (is_username_valid and is_password_valid):
        raise_unauthorized_exception()
