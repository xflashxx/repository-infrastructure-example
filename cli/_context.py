from repository_infrastructure_example.application.context import ApplicationContext


def get_context() -> ApplicationContext:
    """Creates and returns the application context."""
    ctx = ApplicationContext()
    ctx.postgres_client.run_migrations()
    return ctx
