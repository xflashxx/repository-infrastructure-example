import sys

from loguru import logger
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

from repository_infrastructure_example import __appname__, __version__


def set_up_loguru(level: str) -> None:
    """
    Set up Loguru logging with the specified log level.

    :param level: The log level to set.
    :return: None
    """
    logger.remove()
    logger.add(sys.stderr, level=level)


def log_settings(*settings_to_log: BaseModel) -> None:
    """
    Log the settings of the application using rich table.

    :param settings_to_log: The settings to log.
    :return: None
    """
    console = Console()
    table = Table(
        title=f"{__appname__} {__version__}",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Setting")
    table.add_column("Value")

    for settings in settings_to_log:
        # Section header
        table.add_row(f"[bold yellow]{settings.__class__.__name__}[/bold yellow]", "")

        items = list(settings.model_dump().items())
        for i, (env_var_name, value) in enumerate(items, start=1):
            table.add_row(str(env_var_name).upper(), str(value))

            # After the last row of this setting, insert a divider
            if i == len(items):
                table.add_row("─" * 20, "")

    console.print(table)
