"""Service layer orchestrating Hunter API calls and result caching."""

from hunter_sdk.client import DomainSearchClient, EmailFinderClient, EmailVerificationClient
from hunter_sdk.models import DomainSearchResult, EmailFinderResult, EmailVerificationResult
from hunter_sdk.storage import StorageProtocol

_VERIFY_KEY_PREFIX: str = 'verify'
_FINDER_KEY_PREFIX: str = 'finder'
_DOMAIN_KEY_PREFIX: str = 'domain'


class EmailVerificationService:
    """Verifies an email address and caches the result."""

    def __init__(
        self,
        client: EmailVerificationClient,
        storage: StorageProtocol,
    ) -> None:
        """Inject the verification client and storage backend."""
        self._client = client
        self._storage = storage

    def verify(self, email: str) -> EmailVerificationResult:
        """Verify an email address and persist the result."""
        verification_result = self._client.verify(email)
        self._storage.create(f'{_VERIFY_KEY_PREFIX}:{email}', verification_result)
        return verification_result


class EmailFinderService:
    """Finds an email address for a person and caches the result."""

    def __init__(
        self,
        client: EmailFinderClient,
        storage: StorageProtocol,
    ) -> None:
        """Inject the finder client and storage backend."""
        self._client = client
        self._storage = storage

    def find(
        self,
        domain: str,
        first_name: str,
        last_name: str,
    ) -> EmailFinderResult:
        """Find an email for a person and persist the result."""
        finder_result = self._client.find(domain, first_name, last_name)
        self._storage.create(
            f'{_FINDER_KEY_PREFIX}:{domain}:{first_name}:{last_name}',
            finder_result,
        )
        return finder_result


class DomainSearchService:
    """Searches emails by domain and caches the result."""

    def __init__(
        self,
        client: DomainSearchClient,
        storage: StorageProtocol,
    ) -> None:
        """Inject the domain search client and storage backend."""
        self._client = client
        self._storage = storage

    def search(self, domain: str, limit: int = 10) -> DomainSearchResult:
        """Search emails by domain and persist the result."""
        domain_result = self._client.search(domain, limit)
        self._storage.create(f'{_DOMAIN_KEY_PREFIX}:{domain}', domain_result)
        return domain_result
