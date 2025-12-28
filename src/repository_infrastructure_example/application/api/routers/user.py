from uuid import UUID

from fastapi import APIRouter, status

from repository_infrastructure_example.application.api.dependencies import (
    UserServiceDep,
)
from repository_infrastructure_example.application.api.responses import (
    ResourceCreatedResponseModel,
    SuccessResponseModel,
    openapi_responses_from_http_errors,
)
from repository_infrastructure_example.application.api.schemas.user import (
    UserCreateModel,
    UserUpdateModel,
)
from repository_infrastructure_example.domain.user import User
from repository_infrastructure_example.services.organisation import (
    OrganisationNotFoundError,
)
from repository_infrastructure_example.services.user import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserValidationError,
)

user_router = APIRouter(prefix="/v1", tags=["user"])


@user_router.get(
    "/organisations/{organisation_id}/users",
    responses={
        status.HTTP_200_OK: {
            "model": list[User],
            "description": "List of all users of an organisation.",
        },
        **openapi_responses_from_http_errors(OrganisationNotFoundError),
    },
)
def get_users_of_organisation(
    organisation_id: UUID, user_service: UserServiceDep
) -> list[User]:
    """
    Get all users of a specific organisation.
    """
    return user_service.get_users(organisation_id=organisation_id)


@user_router.get(
    "/organisations/{organisation_id}/users/{user_id}",
    responses={
        status.HTTP_200_OK: {
            "model": User,
            "description": "The user object.",
        },
        **openapi_responses_from_http_errors(
            UserNotFoundError, OrganisationNotFoundError
        ),
    },
)
def get_user(
    organisation_id: UUID, user_id: UUID, user_service: UserServiceDep
) -> User:
    """
    Retrieve a user of a specific organisation.
    """
    return user_service.get_user(organisation_id=organisation_id, user_id=user_id)


@user_router.post(
    "/organisations/{organisation_id}/users",
    responses={
        status.HTTP_200_OK: {
            "model": ResourceCreatedResponseModel,
            "description": "User created successfully.",
        },
        **openapi_responses_from_http_errors(
            OrganisationNotFoundError, UserAlreadyExistsError, UserValidationError
        ),
    },
)
def add_user(
    organisation_id: UUID,
    incoming_user: UserCreateModel,
    user_service: UserServiceDep,
) -> ResourceCreatedResponseModel:
    """
    Add a new user to a specific organisation.
    """
    user_id = user_service.add_user(
        first_name=incoming_user.first_name,
        last_name=incoming_user.last_name,
        email=incoming_user.email,
        is_active=incoming_user.is_active,
        organisation_id=organisation_id,
    )
    return ResourceCreatedResponseModel(
        id=user_id, message="User created successfully."
    )


@user_router.put(
    "/organisations/{organisation_id}/users/{user_id}",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponseModel,
            "description": "User updated successfully.",
        },
        **openapi_responses_from_http_errors(
            OrganisationNotFoundError, UserNotFoundError, UserValidationError
        ),
    },
)
def update_user(
    organisation_id: UUID,
    user_id: UUID,
    incoming_user: UserUpdateModel,
    user_service: UserServiceDep,
) -> SuccessResponseModel:
    """
    Update a user in a specific organisation.
    """
    user_service.update_user(
        organisation_id=organisation_id,
        user_id=user_id,
        first_name=incoming_user.first_name,
        last_name=incoming_user.last_name,
        email=incoming_user.email,
        is_active=incoming_user.is_active,
    )
    return SuccessResponseModel(status="User updated successfully.")


@user_router.delete(
    "/organisations/{organisation_id}/users/{user_id}",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponseModel,
            "description": "User deleted successfully.",
        },
        **openapi_responses_from_http_errors(
            OrganisationNotFoundError, UserNotFoundError
        ),
    },
)
def delete_user(
    organisation_id: UUID, user_id: UUID, user_service: UserServiceDep
) -> SuccessResponseModel:
    """
    Delete a user from a specific organisation.
    """
    user_service.delete_user(organisation_id=organisation_id, user_id=user_id)
    return SuccessResponseModel(status="User deleted successfully.")
