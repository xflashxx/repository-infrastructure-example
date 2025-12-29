from faker import Faker

from repository_infrastructure_example.application.api.schemas.user import (
    UserCreateModel,
)

_faker = Faker()


def generate_users(n: int = 1) -> list[UserCreateModel]:
    """
    Generate a list of UserCreateModel instances with random data.

    :param n: The number of users to generate.
    :return: A list of UserCreateModel instances.
    """
    return [
        UserCreateModel(
            first_name=_faker.first_name(),
            last_name=_faker.last_name(),
            email=_faker.email(),
            is_active=_faker.boolean(),
        )
        for _ in range(n)
    ]
