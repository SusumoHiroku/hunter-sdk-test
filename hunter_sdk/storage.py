from typing import Any

from hunter_sdk.exceptions import (
    StorageKeyAlreadyExistsError,
    StorageKeyNotFoundError,
)


class InMemoryStorage:

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def create(self, key: str, stored_item: Any) -> None:
        if key in self._store:
            raise StorageKeyAlreadyExistsError(key)
        self._store[key] = stored_item

    def get(self, key: str) -> Any:
        if key not in self._store:
            raise StorageKeyNotFoundError(key)
        return self._store[key]

    def update(self, key: str, stored_item: Any) -> None:
        if key not in self._store:
            raise StorageKeyNotFoundError(key)
        self._store[key] = stored_item

    def delete(self, key: str) -> None:
        if key not in self._store:
            raise StorageKeyNotFoundError(key)
        self._store.pop(key)

    def list_all(self) -> dict[str, Any]:
        return dict(self._store)
