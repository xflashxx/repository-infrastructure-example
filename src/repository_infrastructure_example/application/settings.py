from typing import Literal

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from repository_infrastructure_example.repositories.backend import RepositoryBackend


class PostgresSettings(BaseModel):
    host: str = Field(description="The host of the Postgresql server.")
    port: int = Field(
        default=5432,
        description="The port to connect to the Postgresql server. Defaults to 5432.",
    )
    username: str = Field(
        default="username", description="The username to authenticate with."
    )
    password: SecretStr = Field(
        description="The password for the database user (optional)."
    )
    name: str = Field(description="The name of the database to connect to.")
    ssl: bool = Field(
        default=False,
        description="Whether to use SSL when connecting to the Postgresql server.",
    )

    def get_connection_uri(self, hide_password: bool = False) -> str:
        """Constructs a Postgresql connection URI.

        :param hide_password: Whether to hide the password in the URI.
            Defaults to False.
        :return: The connection URI.
        """
        password = self.password if hide_password else self.password.get_secret_value()
        connection_uri = f"postgresql+psycopg2://{self.username}:{password}@{self.host}:{self.port}/{self.name}"

        if self.ssl:
            connection_uri += "?sslmode=require"

        return connection_uri


class LoggingSettings(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="The logging level of the application."
    )


class RepositorySettings(BaseModel):
    backend: RepositoryBackend = Field(
        default=RepositoryBackend.POSTGRESQL,
        description="The type of repository to use.",
    )


class ApplicationSettings(BaseSettings):
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)  # pyright: ignore
    repository: RepositorySettings = Field(default_factory=RepositorySettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )
