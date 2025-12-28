from uuid import UUID

from fastapi.testclient import TestClient

from repository_infrastructure_example.application.api.schemas.user import (
    UserCreateModel,
)
from repository_infrastructure_example.domain.user import User
from repository_infrastructure_example.utilities.collections import first_element


def _ensure_no_users_exist(client: TestClient, transient_organisation_id: UUID) -> None:
    response = client.get(f"/v1/organisations/{transient_organisation_id}/users")
    response.raise_for_status()
    assert len(response.json()) == 0, "Users already exist."


def test_inserting_a_user(
    client: TestClient, transient_organisation_id: UUID, user: UserCreateModel
) -> None:
    _ensure_no_users_exist(client, transient_organisation_id)

    # Create a user
    response = client.post(
        f"/v1/organisations/{transient_organisation_id}/users",
        json=user.model_dump(mode="json"),
    )
    response.raise_for_status()
    created_user_id = response.json().get("id")
    assert created_user_id is not None, "User ID was not returned in the response."
    # Get the users
    response = client.get(f"/v1/organisations/{transient_organisation_id}/users")
    response.raise_for_status()
    users = [User.model_validate(u) for u in response.json()]
    assert len(users) == 1, "User was not created successfully."

    received_user = first_element(users)
    assert str(received_user.id) == created_user_id, (
        "Received user ID does not match the created user ID."
    )

    # Clean up by deleting the user
    response = client.delete(
        f"/v1/organisations/{transient_organisation_id}/users/{created_user_id}"
    )
    response.raise_for_status()

    # Verify deletion
    _ensure_no_users_exist(client, transient_organisation_id)


def test_getting_a_user(
    client: TestClient, transient_organisation_id: UUID, transient_user_id: UUID
) -> None:
    response = client.get(
        f"/v1/organisations/{transient_organisation_id}/users/{transient_user_id}"
    )
    response.raise_for_status()
    user = User.model_validate(response.json())
    assert user.id == transient_user_id, (
        "Received user ID does not match the test user ID."
    )


def test_updating_a_user(
    client: TestClient,
    transient_organisation_id: UUID,
    user: UserCreateModel,
    transient_user_id: UUID,
) -> None:
    updated_user = UserCreateModel(
        first_name="NewFirstName",
        last_name="NewLastName",
        email="newemail@example.com",
        is_active=not user.is_active,
    )
    response = client.put(
        f"/v1/organisations/{transient_organisation_id}/users/{transient_user_id}",
        json=updated_user.model_dump(mode="json"),
    )
    response.raise_for_status()

    # Get the updated user
    response = client.get(
        f"/v1/organisations/{transient_organisation_id}/users/{transient_user_id}"
    )
    response.raise_for_status()
    updated_user = User.model_validate(response.json())

    assert updated_user.first_name == updated_user.first_name, (
        "User first name was not updated."
    )
    assert updated_user.last_name == updated_user.last_name, (
        "User last name was not updated."
    )
    assert updated_user.email == updated_user.email, "User email was not updated."
    assert updated_user.is_active == updated_user.is_active, (
        "User active status was not updated."
    )


def test_deleting_a_user(
    client: TestClient, transient_organisation_id: UUID, user: UserCreateModel
) -> None:
    _ensure_no_users_exist(client, transient_organisation_id)

    # Create a user
    response = client.post(
        f"/v1/organisations/{transient_organisation_id}/users",
        json=user.model_dump(mode="json"),
    )
    response.raise_for_status()
    user_id = UUID(response.json()["id"])

    # Delete the user
    response = client.delete(
        f"/v1/organisations/{transient_organisation_id}/users/{user_id}"
    )
    response.raise_for_status()

    # Verify deletion
    _ensure_no_users_exist(client, transient_organisation_id)
