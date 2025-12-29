from repository_infrastructure_example.application.context import ApplicationContext


def get_context() -> ApplicationContext:
    """Creates and returns the application context."""
    ctx = ApplicationContext()
    ctx.clients.postgres.run_migrations()
    return ctx
