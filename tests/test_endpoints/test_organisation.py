from uuid import UUID

from fastapi.testclient import TestClient

from repository_infrastructure_example.application.api.schemas.organisation import (
    OrganisationCreateModel,
)
from repository_infrastructure_example.domain.organisation import Organisation
from repository_infrastructure_example.utilities.collections import first_element


def _ensure_no_organisation_exists(client: TestClient) -> None:
    """Ensure no organisation exists before running tests."""
    response = client.get("/v1/organisations")
    response.raise_for_status()
    assert len(response.json()) == 0, "Organisation already exists."


# Test inserting an organisation
def test_inserting_an_organisation(
    client: TestClient, organisation: OrganisationCreateModel
) -> None:
    _ensure_no_organisation_exists(client)

    # Create an organisation
    response = client.post(
        "/v1/organisations", json=organisation.model_dump(mode="json")
    )
    response.raise_for_status()
    created_organisation_id = response.json()["id"]

    # Get the organisation
    response = client.get("/v1/organisations")
    response.raise_for_status()
    organisations = [Organisation.model_validate(org) for org in response.json()]
    assert len(organisations) == 1, "Organisation was not created successfully."

    received_organisation = first_element(organisations)
    assert str(received_organisation.id) == created_organisation_id, (
        "Received organisation ID does not match the created organisation ID."
    )

    # Delete the organisation after the test
    response = client.delete(f"/v1/organisations/{created_organisation_id}")
    response.raise_for_status()

    # Verify the organisation is deleted
    _ensure_no_organisation_exists(client)


def test_getting_an_organisation(
    client: TestClient, transient_organisation_id: UUID
) -> None:
    response = client.get(f"/v1/organisations/{transient_organisation_id}")
    response.raise_for_status()
    organisation = Organisation.model_validate(response.json())
    assert organisation.id == transient_organisation_id, (
        "Received organisation ID does not match the test organisation ID."
    )


def test_updating_an_organisation(
    client: TestClient,
    organisation: OrganisationCreateModel,
    transient_organisation_id: UUID,
) -> None:
    updated_organisation = OrganisationCreateModel(
        name="New Organisation Name",
        email="updated@email.com",
        is_active=not organisation.is_active,
    )
    response = client.put(
        f"/v1/organisations/{transient_organisation_id}",
        json=updated_organisation.model_dump(mode="json"),
    )
    response.raise_for_status()

    # Get the updated organisation
    response = client.get(f"/v1/organisations/{transient_organisation_id}")
    response.raise_for_status()
    updated_org = Organisation.model_validate(response.json())

    assert updated_org.name == updated_organisation.name, (
        "Organisation name was not updated."
    )
    assert updated_org.email == updated_organisation.email, (
        "Organisation email was not updated."
    )
    assert updated_org.is_active == updated_organisation.is_active, (
        "Organisation active status was not updated."
    )


def test_deleting_an_organisation(
    client: TestClient, organisation: OrganisationCreateModel
) -> None:
    response = client.post(
        "/v1/organisations", json=organisation.model_dump(mode="json")
    )
    response.raise_for_status()
    org_id = response.json()["id"]

    # Delete
    response = client.delete(f"/v1/organisations/{org_id}")
    response.raise_for_status()

    # Verify deletion
    _ensure_no_organisation_exists(client)
