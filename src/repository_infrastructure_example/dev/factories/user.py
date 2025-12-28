from faker import Faker

from repository_infrastructure_example.application.api.schemas.user import (
    UserCreateModel,
)

faker = Faker()


def generate_users(n: int = 1) -> list[UserCreateModel]:
    return [
        UserCreateModel(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            is_active=faker.boolean(),
        )
        for _ in range(n)
    ]
