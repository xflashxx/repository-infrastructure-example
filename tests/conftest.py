from typing import Generator
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from repository_infrastructure_example.application.api.main import app
from repository_infrastructure_example.application.api.schemas.organisation import (
    OrganisationCreateModel,
)
from repository_infrastructure_example.application.api.schemas.user import (
    UserCreateModel,
)
from repository_infrastructure_example.application.context import ApplicationContext
from repository_infrastructure_example.dev.factories.organisation import (
    generate_organisations,
)
from repository_infrastructure_example.dev.factories.user import generate_users
from repository_infrastructure_example.utilities.collections import first_element

# Run database migrations
application_context = ApplicationContext()
application_context.postgres_client.run_migrations()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def organisation() -> OrganisationCreateModel:
    return first_element(generate_organisations())


@pytest.fixture
def transient_organisation_id(
    client: TestClient, organisation: OrganisationCreateModel
) -> Generator[UUID, None, None]:
    # Ensure no organisation exists before the test
    response = client.get("/v1/organisations")
    response.raise_for_status()
    assert len(response.json()) == 0, "Organisations already exist."

    response = client.post(
        "/v1/organisations", json=organisation.model_dump(mode="json")
    )
    response.raise_for_status()
    organisation_id = UUID(response.json()["id"])
    yield organisation_id

    # Cleanup
    response = client.delete(f"/v1/organisations/{organisation_id}")
    response.raise_for_status()


@pytest.fixture
def user() -> UserCreateModel:
    return first_element(generate_users())


@pytest.fixture
def transient_user_id(
    client: TestClient, transient_organisation_id: UUID, user: UserCreateModel
) -> Generator[UUID, None, None]:
    # Ensure no users exists before the test
    response = client.get(f"/v1/organisations/{transient_organisation_id}/users")
    response.raise_for_status()
    assert len(response.json()) == 0, "Users already exists."

    # Create a user
    response = client.post(
        f"/v1/organisations/{transient_organisation_id}/users",
        json=user.model_dump(mode="json"),
    )
    response.raise_for_status()
    user_id = UUID(response.json()["id"])
    yield user_id

    # Cleanup
    response = client.delete(
        f"/v1/organisations/{transient_organisation_id}/users/{user_id}"
    )
    response.raise_for_status()
