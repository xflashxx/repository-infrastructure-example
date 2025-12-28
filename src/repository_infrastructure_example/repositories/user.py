from abc import ABC, abstractmethod
from uuid import UUID

from repository_infrastructure_example.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_users(self, organisation_id: UUID) -> list[User]:
        """
        Get all users in an organisation.

        :param organisation_id: The ID of the organisation.
        :return: A list of users.
        """

    @abstractmethod
    def get_user(self, *, organisation_id: UUID, user_id: UUID) -> User | None:
        """
        Get a user by ID.

        :param organisation_id: The ID of the organisation.
        :param user_id: The ID of the user.
        :return: The user if found, None otherwise.
        """

    @abstractmethod
    def user_exists(self, *, organisation_id: UUID, user_id: UUID) -> bool:
        """
        Check if a user exists in the repository.

        :param organisation_id: The ID of the organisation.
        :param user_id: The ID of the user.
        :return: True if the user exists, False otherwise.
        """

    @abstractmethod
    def user_email_is_available(self, organisation_id: UUID, email: str) -> bool:
        """
        Check if an email is available for a user in the repository.

        :param organisation_id: The ID of the organisation.
        :param email: The email to check.
        :return: True if the email is available, False otherwise.
        """

    @abstractmethod
    def add_or_update_user(self, user: User) -> None:
        """
        Add or update a user in the repository.

        :param user: The user to add or update.
        :return: None
        """

    @abstractmethod
    def delete_user(self, organisation_id: UUID, user_id: UUID) -> None:
        """
        Delete a user from the repository.

        :param organisation_id: The ID of the organisation.
        :param user_id: The ID of the user.
        :return: None
        """
