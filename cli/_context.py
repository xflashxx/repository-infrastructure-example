from repository_infrastructure_example.application.context import ApplicationContext


def get_context() -> ApplicationContext:
    """
    Creates and returns the application context.

    :return: Instance of ApplicationContext.
    """
    ctx = ApplicationContext()
    ctx.clients.postgres.run_migrations(disable_logging=True)
    return ctx
