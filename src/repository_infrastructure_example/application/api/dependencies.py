from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from repository_infrastructure_example.application.context import ApplicationContext
from repository_infrastructure_example.services.organisation import OrganisationService
from repository_infrastructure_example.services.user import UserService


def get_application_context(request: Request) -> ApplicationContext:
    """
    Get the application context from the request.

    :param request: The request object.
    :return: The application context.
    """
    context: ApplicationContext = request.app.state.context
    return context


def get_organisation_service(
    context: ApplicationContext = Depends(get_application_context),
) -> OrganisationService:
    """
    Get the organisation service from the application context.

    :param context: The application context.
    :return: The organisation service.
    """
    return context.services.organisation


def get_user_service(
    context: ApplicationContext = Depends(get_application_context),
) -> UserService:
    """
    Get the user service from the application context.

    :param context: The application context.
    :return: The user service.
    """
    return context.services.user


# FastAPI dependency injection
OrganisationServiceDep = Annotated[
    OrganisationService, Depends(get_organisation_service)
]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
