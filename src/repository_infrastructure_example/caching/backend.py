from enum import StrEnum, auto


class CacheBackend(StrEnum):
    REDIS = auto()
