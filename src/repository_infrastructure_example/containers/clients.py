from redis import Redis

from repository_infrastructure_example.infrastructure.postgres import PostgresClient


class Clients:
    """Container for external service clients."""

    def __init__(
        self,
        postgres_client: PostgresClient,
        redis_client: Redis,
    ) -> None:
        self._postgres: PostgresClient = postgres_client
        self._redis: Redis = redis_client

    @property
    def postgres(self) -> PostgresClient:
        """Get the Postgres client."""
        return self._postgres

    @property
    def redis(self) -> Redis:
        """Get the Redis client."""
        return self._redis
