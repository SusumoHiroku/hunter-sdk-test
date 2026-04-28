"""Exception hierarchy for the Hunter sdk."""


class HunterSDKError(Exception):
    """Base exception for all Hunter sdk errors."""


class HunterRequestError(HunterSDKError):
    """Raised on network-level errors before response is received."""


class HunterAPIError(HunterSDKError):
    """Raised when the API returns non 200 HTTP status code."""

    def __init__(self, status_code: int, message: str) -> None:
        """Store the HTTP status code alongside the error message."""
        self.status_code = status_code
        super().__init__(message)


class HunterResponseError(HunterSDKError):
    """Raised when the API response body cannot be parsed as JSON."""


class StorageError(HunterSDKError):
    """Base exception for in-memory storage errors."""


class StorageKeyNotFoundError(StorageError):
    """Raised when the requested key does not exist in storage."""


class StorageKeyAlreadyExistsError(StorageError):
    """Raised when attempting to create key that already exists."""
