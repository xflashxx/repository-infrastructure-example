from uuid import UUID

from fastapi import APIRouter, status

from repository_infrastructure_example.application.api.dependencies import (
    OrganisationServiceDep,
)
from repository_infrastructure_example.application.api.responses import (
    ResourceCreatedResponseModel,
    SuccessResponseModel,
    openapi_responses_from_http_errors,
)
from repository_infrastructure_example.application.api.schemas.organisation import (
    OrganisationCreateModel,
    OrganisationUpdateModel,
)
from repository_infrastructure_example.domain.organisation import Organisation
from repository_infrastructure_example.services.organisation import (
    OrganisationAlreadyExistsError,
    OrganisationNotFoundError,
    OrganisationValidationError,
)

organisation_router = APIRouter(prefix="/v1", tags=["organisation"])


@organisation_router.get(
    "/organisations",
    responses={
        status.HTTP_200_OK: {
            "model": list[Organisation],
            "description": "List of all organisation objects.",
        },
    },
)
def get_all_organisations(
    organisation_service: OrganisationServiceDep,
) -> list[Organisation]:
    """Get all organisations."""
    return organisation_service.get_organisations()


@organisation_router.get(
    "/organisations/{organisation_id}",
    responses={
        status.HTTP_200_OK: {
            "model": Organisation,
            "description": "The organisation object.",
        },
        **openapi_responses_from_http_errors(OrganisationNotFoundError),
    },
)
def get_organisation(
    organisation_id: UUID,
    organisation_service: OrganisationServiceDep,
) -> Organisation:
    """Get an organisation by ID."""
    return organisation_service.get_organisation(organisation_id)


@organisation_router.post(
    "/organisations",
    responses={
        status.HTTP_200_OK: {
            "model": ResourceCreatedResponseModel,
            "description": "Organisation created successfully.",
        },
        **openapi_responses_from_http_errors(
            OrganisationAlreadyExistsError, OrganisationValidationError
        ),
    },
)
def add_organisation(
    incoming_organisation: OrganisationCreateModel,
    organisation_service: OrganisationServiceDep,
) -> ResourceCreatedResponseModel:
    """Add a new organisation."""
    organisation_id = organisation_service.add_organisation(
        name=incoming_organisation.name,
        email=incoming_organisation.email,
        is_active=incoming_organisation.is_active,
    )
    return ResourceCreatedResponseModel(
        id=organisation_id, message="Organisation created successfully."
    )


# Update the organisation
@organisation_router.put(
    "/organisations/{organisation_id}",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponseModel,
            "description": "The organisation was updated.",
        },
        **openapi_responses_from_http_errors(
            OrganisationNotFoundError, OrganisationValidationError
        ),
    },
)
def update_organisation(
    organisation_id: UUID,
    incoming_organisation: OrganisationUpdateModel,
    organisation_service: OrganisationServiceDep,
) -> SuccessResponseModel:
    """Update an existing organisation."""
    organisation_service.update_organisation(
        name=incoming_organisation.name,
        email=incoming_organisation.email,
        is_active=incoming_organisation.is_active,
        organisation_id=organisation_id,
    )
    return SuccessResponseModel()


@organisation_router.delete(
    "/organisations/{organisation_id}",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponseModel,
            "description": "The organisation was deleted.",
        },
        **openapi_responses_from_http_errors(OrganisationNotFoundError),
    },
)
def delete_organisation(
    organisation_id: UUID,
    organisation_service: OrganisationServiceDep,
) -> SuccessResponseModel:
    """Delete an existing organisation."""
    organisation_service.delete_organisation(organisation_id)
    return SuccessResponseModel()
