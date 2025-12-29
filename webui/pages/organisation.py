"""
Streamlit Page for managing organisations.
"""

import time
from typing import Final

import streamlit as st

from repository_infrastructure_example.application.context import ApplicationContext
from repository_infrastructure_example.services.organisation import (
    OrganisationService,
    OrganisationServiceError,
)

_DEFAULT_RELOAD_TIME_SECONDS: Final[int] = 2


def display_organisations(service: OrganisationService) -> None:
    st.subheader("All organisations")
    organisations = service.get_organisations()
    if not organisations:
        st.info("No organisations found.")
        return

    data = [
        {
            "ID": str(org.id),
            "Name": org.name,
            "Email": org.email,
            "Is Active": org.is_active,
            "Created At": org.created_at,
            "Updated At": org.updated_at,
        }
        for org in organisations
    ]
    st.dataframe(data)  # pyright: ignore[reportUnknownMemberType]


def add_organisation(service: OrganisationService) -> None:
    st.subheader("Add a new organisation")

    with st.form(key="add_organisation_form"):
        name = st.text_input("Organisation Name", max_chars=255)
        email = st.text_input("Email", max_chars=255)
        is_active = st.checkbox("Is Active", value=True)

        submitted = st.form_submit_button("Add organisation")

        if submitted:
            if not all(field.strip() for field in [name, email]):
                st.error("All fields are required.")
                return

            try:
                organisation_id = service.add_organisation(
                    name=name, email=email, is_active=is_active
                )
            except OrganisationServiceError as error:
                st.warning(str(error))
            else:
                st.success(f"Created organisation with ID: {organisation_id}")
                time.sleep(_DEFAULT_RELOAD_TIME_SECONDS)
                st.rerun()


def edit_organisation(service: OrganisationService) -> None:
    st.subheader("Edit Organisation")

    organisations = service.get_organisations()
    if not organisations:
        st.info("No organisations available.")
        return

    selected = st.selectbox(
        "Select organisation to edit", organisations, format_func=lambda o: o.name
    )

    with st.form("edit_organisation_form"):
        name = st.text_input("Name", value=selected.name, max_chars=255)
        email = st.text_input("Email", value=selected.email, max_chars=255)
        is_active = st.checkbox("Is Active", value=selected.is_active)

        submitted = st.form_submit_button("Update")

        if submitted:
            if not all(field.strip() for field in [name, email]):
                st.error("All fields are required.")
                return

            try:
                service.update_organisation(
                    organisation_id=selected.id,
                    name=name,
                    email=email,
                    is_active=is_active,
                )
            except OrganisationServiceError as error:
                st.warning(str(error))
            else:
                st.success("Organisation updated.")
                time.sleep(_DEFAULT_RELOAD_TIME_SECONDS)
                st.rerun()

    # Delete option
    if st.button("Delete Organisation"):
        service.delete_organisation(selected.id)
        st.success("Organisation deleted.")
        time.sleep(_DEFAULT_RELOAD_TIME_SECONDS)
        st.rerun()


def organisation_entry_point() -> None:
    context = ApplicationContext()
    organisation_service = context.services.organisation

    options = ["View organisations", "Add organisation", "Edit organisation"]
    view = st.sidebar.selectbox("Select an action", options)

    match view:
        case "View organisations":
            display_organisations(service=organisation_service)
        case "Add organisation":
            add_organisation(service=organisation_service)
        case "Edit organisation":
            edit_organisation(service=organisation_service)
        case _:
            # handle unexpected values gracefully
            pass
