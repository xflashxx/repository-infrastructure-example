from typing import Callable, ContextManager, override
from uuid import UUID

from sqlmodel import Session, select

from repository_infrastructure_example.domain.user import User
from repository_infrastructure_example.repositories.postgresql.user.dao import (
    PostgresUserDAO,
)
from repository_infrastructure_example.repositories.postgresql.user.mappers import (
    dao_from_user,
    user_from_dao,
)
from repository_infrastructure_example.repositories.user import UserRepository


class PostgresUserRepository(UserRepository):
    _session_factory: Callable[..., ContextManager[Session]]

    def __init__(self, session_factory: Callable[..., ContextManager[Session]]) -> None:
        self._session_factory = session_factory

    @override
    def get_users(self, organisation_id: UUID) -> list[User]:
        statement = select(PostgresUserDAO).where(
            PostgresUserDAO.organisation_id == organisation_id
        )

        with self._session_factory() as session:
            daos = session.exec(statement).all()
            return [user_from_dao(dao) for dao in daos]

    @override
    def get_user(self, *, organisation_id: UUID, user_id: UUID) -> User | None:
        statement = select(PostgresUserDAO).where(
            PostgresUserDAO.id == user_id,
            PostgresUserDAO.organisation_id == organisation_id,
        )
        with self._session_factory() as session:
            dao = session.exec(statement).first()
            if dao is None:
                return None
            return user_from_dao(dao)

    @override
    def user_exists(self, *, organisation_id: UUID, user_id: UUID) -> bool:
        statement = select(PostgresUserDAO.id).where(
            PostgresUserDAO.id == user_id,
            PostgresUserDAO.organisation_id == organisation_id,
        )
        with self._session_factory() as session:
            existing_user_id = session.exec(statement).first()
        return existing_user_id is not None

    @override
    def user_email_is_available(self, organisation_id: UUID, email: str) -> bool:
        statement = select(PostgresUserDAO.id).where(
            PostgresUserDAO.email == email,
            PostgresUserDAO.organisation_id == organisation_id,
        )
        with self._session_factory() as session:
            existing_user_id = session.exec(statement).first()
        return existing_user_id is None

    @override
    def add_or_update_user(self, user: User) -> None:
        dao = dao_from_user(user)
        with self._session_factory() as session:
            session.merge(dao)

    @override
    def delete_user(self, organisation_id: UUID, user_id: UUID) -> None:
        statement = select(PostgresUserDAO).where(
            PostgresUserDAO.id == user_id,
            PostgresUserDAO.organisation_id == organisation_id,
        )

        with self._session_factory() as session:
            dao = session.exec(statement).one()
            session.delete(dao)
