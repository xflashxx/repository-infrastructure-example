from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from repository_infrastructure_example.utilities.identifiers import (
    create_slug,
    generate_uuid,
)
from repository_infrastructure_example.utilities.time import get_current_time_utc


class Organisation(BaseModel):
    id: UUID = Field(
        description="The unique identifier for the organisation.",
        examples=["1ff0bff0-4631-4e7a-a697-d07c07678572"],
    )
    name: str = Field(
        description="The name of the organisation.",
        min_length=3,
        examples=["Acme Inc."],
    )
    slug: str = Field(
        description="The slug of the organisation.", examples=["acme-inc"]
    )
    email: EmailStr = Field(
        description="The email of the organisation.", examples=["info@acme-inc.com"]
    )
    is_active: bool = Field(
        description="Whether the organisation is active.", examples=[True]
    )
    created_at: datetime = Field(
        description="The creation timestamp of the organisation.",
        examples=[datetime(2023, 1, 1, 12, 0, 0)],
    )
    updated_at: datetime = Field(
        description="The update timestamp of the organisation.",
        examples=[datetime(2023, 1, 2, 12, 0, 0)],
    )

    @classmethod
    def create_new(
        cls,
        *,
        name: str,
        email: str,
        is_active: bool,
    ) -> "Organisation":
        """
        Create a new Organisation instance.

        :param name: The name of the organisation.
        :param email: The email of the organisation.
        :param is_active: Whether the organisation is active.
        :param organisation_id: The unique identifier for the organisation.
        :return: A new Organisation instance.
        """
        current_time = get_current_time_utc()
        return cls(
            id=generate_uuid(),
            name=name,
            slug=create_slug(name),
            email=email,
            is_active=is_active,
            created_at=current_time,
            updated_at=current_time,
        )

    @classmethod
    def create_update(
        cls,
        *,
        existing_organisation: "Organisation",
        name: str | None,
        email: str | None,
        is_active: bool | None,
    ) -> "Organisation":
        """
        Create an updated Organisation instance based on an existing one.

        :param existing_organisation: The existing Organisation instance.
        :param name: The new name of the organisation, if updating.
        :param email: The new email of the organisation, if updating.
        :param is_active: The new active status of the organisation, if updating.
        :return: An updated Organisation instance.
        """
        name = name or existing_organisation.name
        email = email or existing_organisation.email
        is_active = (
            is_active if is_active is not None else existing_organisation.is_active
        )

        return cls(
            id=existing_organisation.id,
            name=name,
            slug=create_slug(name),
            email=email,
            is_active=is_active,
            created_at=existing_organisation.created_at,
            updated_at=get_current_time_utc(),
        )
