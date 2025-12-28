from faker import Faker

from repository_infrastructure_example.application.api.schemas.organisation import (
    OrganisationCreateModel,
)

faker = Faker()


def generate_organisations(n: int = 1) -> list[OrganisationCreateModel]:
    return [
        OrganisationCreateModel(
            name=faker.company(),
            email=faker.email(),
            is_active=True,
        )
        for _ in range(n)
    ]
