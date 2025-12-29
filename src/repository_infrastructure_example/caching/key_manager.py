from typing import Final
from uuid import UUID

from repository_infrastructure_example import __appname__, __version__

_PREFIX: Final[str] = f"{__appname__}__{__version__}"


class CacheKeyManager:
    _prefix: str

    def __init__(self, prefix: str = _PREFIX) -> None:
        self._prefix = prefix

    def _construct_key(self, name: str, /) -> str:
        return f"{self._prefix}__{name}"

    @property
    def organisation_ids_key(self) -> str:
        return self._construct_key("organisation_ids")

    def get_user_ids_key(self, organisation_id: UUID) -> str:
        return self._construct_key(f"organisation_id__{organisation_id}__user_ids")
