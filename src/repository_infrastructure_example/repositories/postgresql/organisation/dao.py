from datetime import datetime
from uuid import UUID

from sqlmodel import (
    Field,  # pyright: ignore[reportUnknownVariableType]
    Relationship,
    SQLModel,
)
from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from repository_infrastructure_example.repositories.postgresql.user.dao import (
        PostgresUserDAO,
    )


class PostgresOrganisationDAO(SQLModel, table=True):
    __tablename__ = "organisations"  # pyright: ignore[reportAssignmentType]

    id: UUID = Field(primary_key=True)
    name: str
    slug: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Relations
    users: list["PostgresUserDAO"] = Relationship(
        back_populates="organisation", cascade_delete=True
    )
