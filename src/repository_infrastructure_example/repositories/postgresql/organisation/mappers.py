from repository_infrastructure_example.domain.organisation import Organisation
from repository_infrastructure_example.repositories.postgresql.organisation.dao import (
    PostgresOrganisationDAO,
)


def organisation_from_dao(dao: PostgresOrganisationDAO, /) -> Organisation:
    """
    Maps a DAO object to the organisation domain model.

    :param dao: The DAO object.
    :return: The organisation domain model.
    """
    return Organisation(
        id=dao.id,
        name=dao.name,
        slug=dao.slug,
        email=dao.email,
        is_active=dao.is_active,
        created_at=dao.created_at,
        updated_at=dao.updated_at,
    )


def dao_from_organisation(model: Organisation, /) -> PostgresOrganisationDAO:
    """
    Maps an organisation domain model to a DAO object.

    :param model: The organisation domain model.
    :return: The DAO object.
    """
    return PostgresOrganisationDAO(
        id=model.id,
        name=model.name,
        slug=model.slug,
        email=model.email,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
