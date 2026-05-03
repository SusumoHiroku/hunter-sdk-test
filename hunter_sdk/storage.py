"""Storage abstraction and in-memory implementation for Hunter SDK."""

from typing import Any, Protocol

from hunter_sdk.exceptions import StorageKeyAlreadyExistsError, StorageKeyNotFoundError


class StorageProtocol(Protocol):
    """Structural protocol for key value result storage."""

    def create(self, key: str, stored_item: Any) -> None:
        """Persist a new item under the given key."""

    def get(self, key: str) -> Any:
        """Return the stored item for the given key."""

    def update(self, key: str, stored_item: Any) -> None:
        """Replace the stored item for an existing key."""

    def delete(self, key: str) -> None:
        """Remove the item for the given key."""

    def list_all(self) -> dict[str, Any]:
        """Return all stored items as a dictionary."""


class InMemoryStorage:
    """Thread unsafe in memory key value store for SDK result caching."""

    def __init__(self) -> None:
        """Initialize an empty store."""
        self._store: dict[str, Any] = {}

    def create(self, key: str, stored_item: Any) -> None:
        """Persist a new item, raise if the key already exists."""
        if key in self._store:
            raise StorageKeyAlreadyExistsError(key)
        self._store[key] = stored_item

    def get(self, key: str) -> Any:
        """Return the stored item, raise if the key does not exist."""
        if key not in self._store:
            raise StorageKeyNotFoundError(key)
        return self._store[key]

    def update(self, key: str, stored_item: Any) -> None:
        """Replace an existing item, raise if the key does not exist."""
        if key not in self._store:
            raise StorageKeyNotFoundError(key)
        self._store[key] = stored_item

    def delete(self, key: str) -> None:
        """Remove an item, raise if the key does not exist."""
        if key not in self._store:
            raise StorageKeyNotFoundError(key)
        self._store.pop(key)

    def list_all(self) -> dict[str, Any]:
        """Return a shallow copy of the entire store."""
        return dict(self._store)
