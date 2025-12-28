from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import (
    Field,  # pyright: ignore[reportUnknownVariableType]
    Relationship,
    SQLModel,
    UniqueConstraint,
)

if TYPE_CHECKING:
    from repository_infrastructure_example.repositories.postgresql.organisation.dao import (
        PostgresOrganisationDAO,
    )


class PostgresUserDAO(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore[assignment]
    __table_args__ = (
        UniqueConstraint(
            "organisation_id",
            "email",
            name="uq_user_email",
        ),
    )

    id: UUID = Field(primary_key=True)
    organisation_id: UUID = Field(foreign_key="organisations.id", ondelete="CASCADE")
    first_name: str
    last_name: str
    email: str = Field(index=True)
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Relationships
    organisation: "PostgresOrganisationDAO" = Relationship(back_populates="users")
