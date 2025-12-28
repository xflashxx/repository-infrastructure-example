import time
from typing import Final
from uuid import UUID

import streamlit as st

from repository_infrastructure_example.application.context import ApplicationContext
from repository_infrastructure_example.services.user import (
    UserService,
    UserServiceError,
)

_DEFAULT_RELOAD_TIME_SECONDS: Final[int] = 2


def display_users(*, user_service: UserService, organisation_id: UUID) -> None:
    """
    Displays all users in a Streamlit table.
    """
    st.subheader("All Users")
    users = user_service.get_users(organisation_id=organisation_id)

    if not users:
        st.info("No users found.")
        return

    # Dynamically create table data
    data = [
        {
            "ID": str(user.id),
            "Organisation ID": str(user.organisation_id),
            "First Name": user.first_name,
            "Last Name": user.last_name,
            "Email": user.email,
            "Is Active": user.is_active,
            "Created At": user.created_at,
            "Updated At": user.updated_at,
        }
        for user in users
    ]
    st.dataframe(data)  # pyright: ignore[reportUnknownMemberType]


def add_user(user_service: UserService, organisation_id: UUID) -> None:
    """
    Renders a form to add a new user.
    """
    st.subheader("Add a New User")

    with st.form(key="add_user_form"):
        first_name: str = st.text_input("First Name", max_chars=50)
        last_name: str = st.text_input("Last Name", max_chars=50)
        email: str = st.text_input("Email", max_chars=255)
        is_active: bool = st.checkbox("Is Active", value=True)

        submitted: bool = st.form_submit_button("Add User")

        if submitted:
            if not all(field.strip() for field in [first_name, last_name, email]):
                st.error("All fields are required.")
                return

            try:
                user_service.add_user(
                    organisation_id=organisation_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    is_active=is_active,
                )
            except UserServiceError as error:
                st.warning(str(error))
            else:
                st.success("User added successfully.")
                time.sleep(_DEFAULT_RELOAD_TIME_SECONDS)
                st.rerun()


def edit_user(*, service: UserService, organisation_id: UUID) -> None:
    st.subheader("Edit User")

    users = service.get_users(organisation_id=organisation_id)
    if not users:
        st.info("No users available.")
        return

    selected_user = st.selectbox(
        "Select user to edit",
        users,
        format_func=lambda u: f"{u.first_name} {u.last_name}",
    )

    with st.form("edit_user_form"):
        first_name = st.text_input("First Name", value=selected_user.first_name)
        last_name = st.text_input("Last Name", value=selected_user.last_name)
        email = st.text_input("Email", value=selected_user.email)
        is_active = st.checkbox("Is Active", value=selected_user.is_active)

        submitted = st.form_submit_button("Update")

        if submitted:
            if not all(field.strip() for field in [first_name, last_name, email]):
                st.error("All fields are required.")
                return

            try:
                service.update_user(
                    organisation_id=organisation_id,
                    user_id=selected_user.id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    is_active=is_active,
                )
            except UserServiceError as error:
                st.warning(str(error))
            else:
                st.success("User updated.")
                time.sleep(_DEFAULT_RELOAD_TIME_SECONDS)
                st.rerun()

    # Delete option
    if st.button("Delete User"):
        service.delete_user(organisation_id=organisation_id, user_id=selected_user.id)
        st.success("User deleted.")
        time.sleep(_DEFAULT_RELOAD_TIME_SECONDS)
        st.rerun()
        return


def user_entry_point() -> None:
    """
    Main entry point of the Streamlit user management app.
    """
    application_context = ApplicationContext()
    user_service = application_context.services.user
    organisation_service = application_context.services.organisation

    # Fetch all organisations
    all_organisations = organisation_service.get_all_organisations()
    if not all_organisations:
        st.warning("No organisations found. Please add an organisation first.")
        st.stop()

    # Select an organisation
    organisation_id_by_name = {
        f"{organisation.name} ({organisation.id})": organisation.id
        for organisation in all_organisations
    }
    selected_organisation_name = st.sidebar.selectbox(
        "Select an organisation",
        list(organisation_id_by_name.keys()),
    )
    selected_organisation_id = organisation_id_by_name[selected_organisation_name]

    view: str = st.sidebar.radio("Options", ["View Users", "Add User", "Edit User"])
    st.sidebar.divider()

    match view:
        case "View Users":
            display_users(
                user_service=user_service,
                organisation_id=selected_organisation_id,
            )
        case "Add User":
            add_user(
                user_service=user_service,
                organisation_id=selected_organisation_id,
            )
        case "Edit User":
            edit_user(
                service=user_service,
                organisation_id=selected_organisation_id,
            )
        case _:
            pass
