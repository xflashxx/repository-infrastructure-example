from uuid import UUID

from fastapi import status
from typing_extensions import overload

from repository_infrastructure_example.domain.organisation import Organisation
from repository_infrastructure_example.exceptions import HTTPError
from repository_infrastructure_example.repositories.organisation import (
    OrganisationRepository,
)
from repository_infrastructure_example.utilities.identifiers import create_slug


class OrganisationServiceError(Exception):
    """Base class for all organisation service errors."""


class OrganisationNotFoundError(OrganisationServiceError, HTTPError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Organisation not found"

    def __init__(self, organisation_id: UUID) -> None:
        self.detail = f"Organisation with ID '{organisation_id}' not found."
        super().__init__(status_code=self.status_code, detail=self.detail)


class OrganisationAlreadyExistsError(OrganisationServiceError, HTTPError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Organisation already exists"

    @overload
    def __init__(self, *, organisation_id: UUID) -> None: ...

    @overload
    def __init__(self, *, name: str) -> None: ...

    def __init__(
        self, *, organisation_id: UUID | None = None, name: str | None = None
    ) -> None:
        if organisation_id is not None:
            self.detail = f"Organisation with ID '{organisation_id}' already exists."
        elif name is not None:
            self.detail = f"Organisation with name '{name}' already exists."
        else:
            raise ValueError("Either organisation id or name must be provided")

        super().__init__(status_code=self.status_code, detail=self.detail)


class OrganisationValidationError(OrganisationServiceError, HTTPError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Organisation validation error"

    def __init__(self, message: str) -> None:
        self.detail = f"Organisation validation error: {message}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class OrganisationService:
    _repository: OrganisationRepository

    def __init__(
        self,
        repository: OrganisationRepository,
    ) -> None:
        self._repository = repository

    def ensure_organisation_exists(self, organisation_id: UUID) -> None:
        """
        Ensure that an organisation with the given ID exists.

        :param organisation_id: The ID of the organisation.
        :raises OrganisationNotFoundError: If the organisation does not exist.
        """
        if not self._repository.organisation_exists(organisation_id):
            raise OrganisationNotFoundError(organisation_id)

    def get_all_organisations(self) -> list[Organisation]:
        """
        Get all organisations.

        :return: List of all organisations.
        """
        return self._repository.get_all_organisations()

    def get_organisation(self, organisation_id: UUID) -> Organisation:
        """
        Get an organisation by its ID.

        :param organisation_id: The ID of the organisation.
        :return: The organisation if found, else None.
        """
        organisation = self._repository.get_organisation(organisation_id)
        if organisation is None:
            raise OrganisationNotFoundError(organisation_id)
        return organisation

    def add_organisation(self, *, name: str, email: str, is_active: bool) -> UUID:
        """
        Add a new organisation.

        :param name: The name of the organisation.
        :param email: The email of the organisation.
        :param is_active: Whether the organisation is active.
        :return: The ID of the newly created organisation.
        :raises OrganisationAlreadyExistsError: If an organisation with the same
            name already exists.
        :raises OrganisationValidationError: If the organisation data is invalid.
        """
        existing = self._repository.get_organisation_by_slug(create_slug(name))
        if existing:
            raise OrganisationAlreadyExistsError(name=name)

        try:
            organisation = Organisation.create_new(
                name=name,
                email=email,
                is_active=is_active,
            )
        except ValueError as error:
            raise OrganisationValidationError(str(error)) from error

        self._repository.add_or_update_organisation(organisation)

        return organisation.id

    def update_organisation(
        self,
        *,
        organisation_id: UUID,
        name: str | None = None,
        email: str | None = None,
        is_active: bool | None = None,
    ) -> None:
        """
        Update an existing organisation.

        :param organisation_id: The ID of the organisation to update.
        :param name: Optional new name of the organisation. If None, retains existing
            name. Defaults to None.
        :param email: Optional new email of the organisation. If None, retains existing
            email. Defaults to None.
        :param is_active: Optional new active status of the organisation. If None,
            retains existing active status. Defaults to None.
        :return: None
        :raises OrganisationNotFoundError: If the organisation does not exist.
        :raises OrganisationAlreadyExistsError: If an organisation with the same
            name already exists.
        :raises OrganisationValidationError: If the updated organisation data is
            invalid.
        """
        # Fetch existing organisation
        existing = self._repository.get_organisation(organisation_id)
        if not existing:
            raise OrganisationNotFoundError(organisation_id)

        # Check if we update anything
        if all(
            field is None
            for field in (
                name,
                email,
                is_active,
            )
        ):
            return

        # Ensure the organisation name is not already taken
        if name is not None and existing.name != name:
            # Check if another organisation with the same name already exists
            # TODO: replace method below with dedicated method like 'check if name is available'
            existing_by_name = self._repository.get_organisation_by_name(name)
            if existing_by_name:
                raise OrganisationAlreadyExistsError(
                    organisation_id=existing_by_name.id
                )

        # Create updated organisation instance
        try:
            organisation = Organisation.create_update(
                existing_organisation=existing,
                name=name,
                email=email,
                is_active=is_active,
            )
        except ValueError as error:
            raise OrganisationValidationError(str(error)) from error

        self._repository.add_or_update_organisation(organisation)

    def delete_organisation(self, organisation_id: UUID) -> None:
        """
        Delete an organisation by its ID.

        :param organisation_id: The ID of the organisation to delete.
        :return: None
        :raises OrganisationNotFoundError: If the organisation does not exist.
        """
        self.ensure_organisation_exists(organisation_id)
        self._repository.delete_organisation(organisation_id)
