from uuid import UUID

from fastapi import status

from repository_infrastructure_example.caching.key_manager import CacheKeyManager
from repository_infrastructure_example.caching.cache import CacheService
from repository_infrastructure_example.domain.user import User
from repository_infrastructure_example.exceptions import HTTPError
from repository_infrastructure_example.repositories.user import UserRepository
from repository_infrastructure_example.services.organisation import OrganisationService


class UserServiceError(Exception):
    """Base class for exceptions in the UserService module."""


class UserAlreadyExistsError(UserServiceError, HTTPError):
    """Exception raised when a user already exists."""

    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"

    def __init__(self, email: str) -> None:
        self.detail = f"User with email '{email}' already exists"
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotFoundError(UserServiceError, HTTPError):
    """Exception raised when a user is not found."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"

    def __init__(self, user_id: UUID) -> None:
        self.detail = f"User with id '{user_id}' not found"
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserValidationError(UserServiceError, HTTPError):
    """Exception raised when a user is not valid."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "User validation error"

    def __init__(self, message: str) -> None:
        self.detail = f"User validation error: {message}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserService:
    _organisation_service: OrganisationService
    _repository: UserRepository
    _cache_service: CacheService
    _cache_key_manager: CacheKeyManager

    def __init__(
        self,
        *,
        organisation_service: OrganisationService,
        user_repository: UserRepository,
        cache_service: CacheService,
        cache_key_manager: CacheKeyManager,
    ) -> None:
        self._organisation_service = organisation_service
        self._repository = user_repository
        self._cache_service = cache_service
        self._cache_key_manager = cache_key_manager

    def ensure_user_exists(self, *, organisation_id: UUID, user_id: UUID) -> None:
        # Try to get all user IDs from cache
        cached_user_ids = self._cache_service.get_set(
            self._cache_key_manager.get_user_ids_key(organisation_id)
        )
        if cached_user_ids is not None:
            if str(user_id) in cached_user_ids:
                return
            raise UserNotFoundError(user_id)

        # Fetch from the repository
        user_ids = self._repository.get_user_ids(organisation_id)

        # Store user IDs in cache
        self._cache_service.store_set(
            key=self._cache_key_manager.get_user_ids_key(organisation_id),
            value=set(map(str, user_ids)),
        )

        # Check if the user exists
        if user_id not in user_ids:
            raise UserNotFoundError(user_id)

    def get_users(self, organisation_id: UUID) -> list[User]:
        self._organisation_service.ensure_organisation_exists(organisation_id)
        return self._repository.get_users(organisation_id)

    def get_user(self, *, organisation_id: UUID, user_id: UUID) -> User:
        self._organisation_service.ensure_organisation_exists(organisation_id)

        user = self._repository.get_user(
            user_id=user_id, organisation_id=organisation_id
        )
        if user is None:
            raise UserNotFoundError(user_id)

        return user

    def email_is_available(self, *, organisation_id: UUID, email: str) -> bool:
        return self._repository.user_email_is_available(
            organisation_id=organisation_id, email=email
        )

    def add_user(
        self,
        *,
        organisation_id: UUID,
        first_name: str,
        last_name: str,
        email: str,
        is_active: bool,
    ) -> UUID:
        self._organisation_service.ensure_organisation_exists(organisation_id)

        if not self.email_is_available(organisation_id=organisation_id, email=email):
            raise UserAlreadyExistsError(email)

        try:
            user = User.create_new(
                organisation_id=organisation_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=is_active,
            )
        except ValueError as error:
            raise UserValidationError(str(error)) from error

        self._repository.add_or_update_user(user)

        # Invalidate the cache
        self._cache_service.delete_key(
            self._cache_key_manager.get_user_ids_key(organisation_id)
        )

        return user.id

    def update_user(
        self,
        *,
        organisation_id: UUID,
        user_id: UUID,
        first_name: str | None,
        last_name: str | None,
        email: str | None,
        is_active: bool | None,
    ) -> User:
        self._organisation_service.ensure_organisation_exists(organisation_id)

        existing = self._repository.get_user(
            user_id=user_id, organisation_id=organisation_id
        )
        if existing is None:
            raise UserNotFoundError(user_id)

        if (
            email is not None
            and existing.email != email
            and not self.email_is_available(
                organisation_id=organisation_id, email=email
            )
        ):
            raise UserAlreadyExistsError(email)

        try:
            user = User.create_update(
                existing_user=existing,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=is_active,
            )
        except ValueError as error:
            raise UserValidationError(str(error)) from error

        self._repository.add_or_update_user(user)
        return user

    def delete_user(self, *, organisation_id: UUID, user_id: UUID) -> None:
        self._organisation_service.ensure_organisation_exists(
            organisation_id=organisation_id
        )
        self.ensure_user_exists(organisation_id=organisation_id, user_id=user_id)
        self._repository.delete_user(organisation_id=organisation_id, user_id=user_id)
        self._cache_service.delete_key(
            self._cache_key_manager.get_user_ids_key(organisation_id)
        )
