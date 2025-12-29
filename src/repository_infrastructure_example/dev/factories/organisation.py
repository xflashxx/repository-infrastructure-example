from faker import Faker

from repository_infrastructure_example.application.api.schemas.organisation import (
    OrganisationCreateModel,
)

_faker = Faker()


def generate_organisations(n: int = 1) -> list[OrganisationCreateModel]:
    """
    Generate a list of OrganisationCreateModel instances with random data.

    :param n: The number of organisations to generate.
    :return: A list of OrganisationCreateModel instances.
    """
    return [
        OrganisationCreateModel(
            name=_faker.company(),
            email=_faker.email(),
            is_active=True,
        )
        for _ in range(n)
    ]
