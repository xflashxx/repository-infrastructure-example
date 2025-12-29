import streamlit as st

from repository_infrastructure_example import __version__
from repository_infrastructure_example.application.context import ApplicationContext
from pages.organisation import organisation_entry_point
from pages.user import user_entry_point

st.set_page_config(
    page_title="Developer Web Interface", layout="wide", page_icon="🧑‍💻"
)

# Define the pages for the application
organisation_page = st.Page(
    organisation_entry_point, title="Organisation Management", icon="🏨"
)
user_page = st.Page(user_entry_point, title="User Management", icon="👥")

# Add a sidebar with the application name and version
st.sidebar.header("Developer Web Interface")
st.sidebar.text(f"Version: {__version__}")
st.sidebar.divider()

# Initialize the sidebar navigation
pg = st.navigation({"Navigation": [organisation_page, user_page]})

if __name__ == "__main__":
    # Set up the application
    application_context = ApplicationContext()
    application_context.log_settings()
    application_context.clients.postgres.run_migrations()

    # Run Streamlit
    pg.run()
