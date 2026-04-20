
class HunterSDKError(Exception):
    """Base sdk exception."""


class HunterRequestError(HunterSDKError):
    """Raised on network-level errors."""


class HunterAPIError(HunterSDKError):

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(message)


class HunterResponseError(HunterSDKError):
    """Raised when the api response cannot be parsed"""


class StorageError(HunterSDKError):
    """Base storage exception"""


class StorageKeyNotFoundError(StorageError):
    """Raised when a key does not exist in storage"""


class StorageKeyAlreadyExistsError(StorageError):
    """Raised when a key already exists in storage"""
