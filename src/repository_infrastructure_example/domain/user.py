from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from repository_infrastructure_example.utilities.identifiers import generate_uuid
from repository_infrastructure_example.utilities.time import get_current_time_utc


class User(BaseModel):
    id: UUID = Field(
        description="The unique identifier of the user.",
        examples=["b837d929-73f5-4245-8b9d-df8e50b66cb9"],
    )
    organisation_id: UUID = Field(
        description="The unique identifier of the organisation.",
        examples=["1ff0bff0-4631-4e7a-a697-d07c07678572"],
    )
    first_name: str = Field(description="First name of the user.", examples=["John"])
    last_name: str = Field(description="Last name of the user.", examples=["Doe"])
    email: str = Field(description="Email of the user.", examples=["john.doe@acme.com"])
    is_active: bool = Field(description="Whether the user is active.", examples=[True])
    created_at: datetime = Field(
        description="The creation timestamp of the user.",
        examples=[datetime(2023, 1, 1, 12, 0, 0)],
    )
    updated_at: datetime = Field(
        description="The update timestamp of the user.",
        examples=[datetime(2023, 1, 2, 12, 0, 0)],
    )

    @classmethod
    def create_new(
        cls,
        *,
        organisation_id: UUID,
        first_name: str,
        last_name: str,
        email: str,
        is_active: bool,
    ) -> "User":
        """
        Create a new User instance.

        :param organisation_id: The unique identifier for the organisation.
        :param first_name: The first name of the user.
        :param last_name: The last name of the user.
        :param email: The email of the user.
        :param is_active: Whether the user is active.
        :return: A new User instance.
        """
        current_time = get_current_time_utc()
        return cls(
            id=generate_uuid(),
            organisation_id=organisation_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
            created_at=current_time,
            updated_at=current_time,
        )

    @classmethod
    def create_update(
        cls,
        *,
        existing_user: "User",
        first_name: str | None,
        last_name: str | None,
        email: str | None,
        is_active: bool | None,
    ) -> "User":
        first_name = first_name or existing_user.first_name
        last_name = last_name or existing_user.last_name
        email = email or existing_user.email
        is_active = is_active if is_active is not None else existing_user.is_active

        return cls(
            id=existing_user.id,
            organisation_id=existing_user.organisation_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
            created_at=existing_user.created_at,
            updated_at=get_current_time_utc(),
        )
