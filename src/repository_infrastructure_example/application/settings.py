from typing import Literal

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from repository_infrastructure_example.repositories.backend import DatabaseBackend


class DatabaseSettings(BaseModel):
    host: str = Field(
        default="localhost", description="The host of the Postgresql server."
    )
    port: int = Field(
        default=5432,
        description="The port to connect to the Postgresql server. Defaults to 5432.",
    )
    username: str = Field(
        default="username", description="The username to authenticate with."
    )
    password: SecretStr | None = Field(
        default=None, description="The password for the database user (optional)."
    )
    name: str = Field(
        default="database_name", description="The name of the database to connect to."
    )

    def get_connection_uri(self, hide_password: bool = False) -> str:
        """Constructs a Postgresql connection URI.

        :param hide_password: Whether to hide the password in the URI.
            Defaults to False.
        :return: The connection URI.
        """
        if hide_password:
            password = self.password if self.password is not None else None
        else:
            password = (
                self.password.get_secret_value() if self.password is not None else None
            )

        auth = f"{self.username}:{password}" if password is not None else self.username

        return f"postgresql+psycopg2://{auth}@{self.host}:{self.port}/{self.name}"


class LoggingSettings(BaseModel):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="The logging level of the application."
    )


class RepositorySettings(BaseModel):
    backend: DatabaseBackend = Field(
        default=DatabaseBackend.POSTGRESQL, description="The type of repository to use."
    )


class ApplicationSettings(BaseSettings):
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    repository: RepositorySettings = Field(default_factory=RepositorySettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )
