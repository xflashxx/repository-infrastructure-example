from repository_infrastructure_example.domain.user import User
from repository_infrastructure_example.repositories.postgresql.user.dao import (
    PostgresUserDAO,
)


def user_from_dao(dao: PostgresUserDAO, /) -> User:
    """
    Maps a DAO object to the user domain model.

    :param dao: The DAO object.
    :return: The user domain model.
    """
    return User(
        id=dao.id,
        organisation_id=dao.organisation_id,
        first_name=dao.first_name,
        last_name=dao.last_name,
        email=dao.email,
        is_active=dao.is_active,
        created_at=dao.created_at,
        updated_at=dao.updated_at,
    )


def dao_from_user(model: User, /) -> PostgresUserDAO:
    """
    Maps a user domain model to a DAO object.

    :param model: The user domain model.
    :return: The DAO object.
    """
    return PostgresUserDAO(
        id=model.id,
        organisation_id=model.organisation_id,
        first_name=model.first_name,
        last_name=model.last_name,
        email=model.email,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
