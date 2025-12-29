from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    PositiveFloat,
    PositiveInt,
    SecretStr,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

from repository_infrastructure_example.caching.backend import CacheBackend
from repository_infrastructure_example.repositories.backend import RepositoryBackend


class APISettings(BaseModel):
    require_authentication: bool = Field(
        default=False,
        description="Whether the API requires authentication for access.",
    )
    api_key: SecretStr | None = Field(
        default=None,
        description="The API key required for authentication if authentication is enabled.",
    )
    documentation_username: str | None = Field(
        default=None,
        description="The username for accessing the API documentation (if protected).",
    )
    documentation_password: SecretStr | None = Field(
        default=None,
        description="The password for accessing the API documentation (if protected).",
    )

    @model_validator(mode="after")
    def check_api_key(self) -> Self:
        """
        Validate that an API key is provided if authentication is required.

        :raises ValueError: If authentication is required but no API key is set.
        :return: The validated instance.
        """
        if not self.require_authentication:
            return self

        if not self.api_key:
            raise ValueError("API key must be set if authentication is required.")

        return self

    @model_validator(mode="after")
    def check_documentation_credentials(self) -> Self:
        """
        Validate that both username and password are provided for documentation access.

        :raises ValueError: If only one of the documentation credentials is set.
        :return: The validated instance.
        """
        if not self.require_authentication:
            return self

        if not self.documentation_username:
            raise ValueError(
                "Documentation username must be set if authentication is required."
            )
        if not self.documentation_password:
            raise ValueError(
                "Documentation password must be set if authentication is required."
            )
        return self


class PostgresSettings(BaseModel):
    host: str = Field(description="The host of the Postgresql server.")
    port: int = Field(
        default=5432,
        description="The port to connect to the Postgresql server. Defaults to 5432.",
    )
    username: str = Field(description="The username to authenticate with.")
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


class CacheSettings(BaseModel):
    backend: CacheBackend = Field(
        default=CacheBackend.REDIS, description="The type of cache to use."
    )
    keys_ttl: PositiveInt | None = Field(
        default=None,
        description="The default time-to-live (TTL) in seconds for Redis keys."
        "If None, keep keys forever.",
    )


class RedisSettings(BaseModel):
    host: str = Field(description="The host of the Redis server.")
    port: int = Field(
        default=6379,
        description="The port to connect to the Redis server. Defaults to 6379.",
    )
    password: SecretStr | None = Field(
        default=None,
        description="The password for the Redis server (optional).",
    )
    timeout: PositiveFloat = Field(
        default=0.5,
        description="The timeout in seconds for Redis operations. Defaults to 0.5 seconds.",
    )
    health_check_interval: PositiveInt = Field(
        default=30,
        description="The interval in seconds for Redis health checks. Defaults to 30 seconds.",
    )
    client_side_caching: bool = Field(
        default=False,
        description="Whether to enable client-side caching for Redis. Defaults to False.",
    )


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
    api: APISettings = Field(default_factory=APISettings)
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)  # pyright: ignore
    cache: CacheSettings = Field(default_factory=CacheSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)  # pyright: ignore
    repository: RepositorySettings = Field(default_factory=RepositorySettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )
