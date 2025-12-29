from abc import ABC, abstractmethod
from uuid import UUID

from repository_infrastructure_example.domain.organisation import Organisation


class OrganisationRepository(ABC):
    @abstractmethod
    def organisation_exists(self, organisation_id: UUID) -> bool:
        """
        Check if an organisation with the given ID exists.

        :param organisation_id: The ID of the organisation.
        :return: True if the organisation exists, False otherwise.
        """

    @abstractmethod
    def get_organisations(self) -> list[Organisation]:
        """
        Get all organisations.

        :return: List of all organisations.
        """

    @abstractmethod
    def get_organisation_ids(self) -> set[UUID]:
        """
        Get all organisation IDs.

        :return: Set of all organisation IDs.
        """

    @abstractmethod
    def get_organisation(self, organisation_id: UUID) -> Organisation | None:
        """
        Get an organisation by its ID.

        :param organisation_id: The ID of the organisation.
        :return: The organisation if found, None otherwise.
        """

    @abstractmethod
    def get_organisation_by_slug(self, slug: str) -> Organisation | None:
        """
        Get an organisation by its slug.

        :param slug: The slug of the organisation.
        :return: The organisation if found, None otherwise.
        """

    @abstractmethod
    def get_organisation_by_name(self, name: str) -> Organisation | None:
        """
        Get an organisation by its name.

        :param name: The name of the organisation.
        :return: The organisation if found, None otherwise.
        """

    @abstractmethod
    def add_or_update_organisation(self, organisation: Organisation) -> None:
        """
        Add a new organisation or update an existing one.

        :param organisation: The organisation to add or update.
        """

    @abstractmethod
    def delete_organisation(self, organisation_id: UUID) -> None:
        """
        Delete an organisation by its ID.

        :param organisation_id: The ID of the organisation to delete.
        """
