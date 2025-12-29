from abc import ABC, abstractmethod
from typing import Set, final

from loguru import logger


class CacheService(ABC):
    @abstractmethod
    def _store_set(self, *, key: str, value: Set[str]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _get_set(self, key: str, /) -> set[str] | None:
        raise NotImplementedError()

    @abstractmethod
    def _delete_key(self, key: str, /) -> None:
        raise NotImplementedError()

    @final
    def store_set(self, *, key: str, value: Set[str]) -> None:
        """
        Store a set of strings in the cache under the given key.

        :param key: The cache key.
        :param value: The set of strings to store.
        :return: None
        """
        try:
            self._store_set(key=key, value=value)
        except Exception as error:
            logger.error(f"Failed to store set using key '{key}': {str(error)}")

    @final
    def get_set(self, key: str, /) -> set[str] | None:
        """
        Retrieve a set of strings from the cache by the given key.

        :param key: The cache key.
        :return: The set of strings if found, otherwise None.
        """
        try:
            return self._get_set(key)
        except Exception as error:
            logger.error(f"Failed to retrieve set using key '{key}': {str(error)}")

    @final
    def delete_key(self, key: str, /) -> None:
        """
        Delete the cache entry for the given key.

        :param key: The cache key.
        :return: None
        """
        try:
            self._delete_key(key)
        except Exception as error:
            logger.error(f"Failed to delete key '{key}': {str(error)}")
