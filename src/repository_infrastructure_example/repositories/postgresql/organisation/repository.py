from typing import Callable, ContextManager
from uuid import UUID

from sqlmodel import Session, select
from typing_extensions import override

from repository_infrastructure_example.domain.organisation import Organisation
from repository_infrastructure_example.repositories.organisation import (
    OrganisationRepository,
)
from repository_infrastructure_example.repositories.postgresql.organisation.dao import (
    PostgresOrganisationDAO,
)
from repository_infrastructure_example.repositories.postgresql.organisation.mappers import (
    dao_from_organisation,
    organisation_from_dao,
)


class PostgresOrganisationRepository(OrganisationRepository):
    _session_factory: Callable[..., ContextManager[Session]]

    def __init__(self, session_factory: Callable[..., ContextManager[Session]]) -> None:
        self._session_factory = session_factory

    @override
    def organisation_exists(self, organisation_id: UUID) -> bool:
        statement = select(PostgresOrganisationDAO.id).where(
            PostgresOrganisationDAO.id == organisation_id
        )
        with self._session_factory() as session:
            existing_organisation_id = session.exec(statement).first()

        return False if existing_organisation_id is None else True

    @override
    def get_all_organisations(self) -> list[Organisation]:
        statement = select(PostgresOrganisationDAO)

        with self._session_factory() as session:
            results = session.exec(statement)
            daos = list(results.all())
            return [organisation_from_dao(dao) for dao in daos]

    @override
    def get_organisation(self, organisation_id: UUID) -> Organisation | None:
        statement = select(PostgresOrganisationDAO).where(
            PostgresOrganisationDAO.id == organisation_id
        )

        with self._session_factory() as session:
            dao = session.exec(statement).first()
            if dao is None:
                return None
            return organisation_from_dao(dao)

    @override
    def get_organisation_by_slug(self, slug: str) -> Organisation | None:
        statement = select(PostgresOrganisationDAO).where(
            PostgresOrganisationDAO.slug == slug
        )

        with self._session_factory() as session:
            dao = session.exec(statement).first()
            if dao is None:
                return None
            return organisation_from_dao(dao)

    @override
    def get_organisation_by_name(self, name: str) -> Organisation | None:
        statement = select(PostgresOrganisationDAO).where(
            PostgresOrganisationDAO.name == name
        )

        with self._session_factory() as session:
            dao = session.exec(statement).first()
            if dao is None:
                return None
            return organisation_from_dao(dao)

    @override
    def add_or_update_organisation(self, organisation: Organisation) -> None:
        dao = dao_from_organisation(organisation)

        with self._session_factory() as session:
            session.merge(dao)

    @override
    def delete_organisation(self, organisation_id: UUID) -> None:
        statement = select(PostgresOrganisationDAO).where(
            PostgresOrganisationDAO.id == organisation_id
        )

        with self._session_factory() as session:
            organisation = session.exec(statement).one()
            session.delete(organisation)
