from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from repository_infrastructure_example.application.context import ApplicationContext
from repository_infrastructure_example.services.organisation import OrganisationService
from repository_infrastructure_example.services.user import UserService


def get_application_context(request: Request) -> ApplicationContext:
    context: ApplicationContext = request.app.state.context
    return context


def get_organisation_service(
    context: ApplicationContext = Depends(get_application_context),
) -> OrganisationService:
    return context.services.organisation


def get_user_service(
    context: ApplicationContext = Depends(get_application_context),
) -> UserService:
    return context.services.user


OrganisationServiceDep = Annotated[
    OrganisationService, Depends(get_organisation_service)
]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
