from redis import Redis
from redis.cache import CacheConfig

from repository_infrastructure_example.application.settings import RedisSettings


def get_redis_client(settings: RedisSettings) -> Redis:
    """
    Creates and returns a Redis client based on the provided settings.

    :param settings: The Redis settings.
    :return: A Redis client instance.
    """
    password = (
        settings.password.get_secret_value() if settings.password is not None else None
    )
    return Redis(
        host=settings.host,
        port=settings.port,
        password=password,
        socket_timeout=settings.timeout,
        socket_connect_timeout=settings.timeout,
        health_check_interval=settings.health_check_interval,
        protocol=3 if settings.client_side_caching else 2,
        cache_config=CacheConfig() if settings.client_side_caching else None,
        socket_keepalive=True,
        decode_responses=True,
    )
