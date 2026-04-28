"""Service layer orchestrating Hunter API calls and result."""

from hunter_sdk.client import HunterClient
from hunter_sdk.models import (
    DomainSearchResult,
    EmailFinderResult,
    EmailVerificationResult,
)
from hunter_sdk.storage import InMemoryStorage


class HunterService:
    """Orchestrates Hunter API calls and persists results to storage."""

    def __init__(
        self,
        client: HunterClient,
        storage: InMemoryStorage,
    ) -> None:
        """Inject the HTTP client and storage backend."""
        self._client = client
        self._storage = storage

    def verify_email(self, email: str) -> EmailVerificationResult:
        """Verify an email address and cache the result."""
        verification_result = self._client.verify_email(email)
        self._storage.create(f'verify:{email}', verification_result)
        return verification_result

    def find_email(
        self,
        domain: str,
        first_name: str,
        last_name: str,
    ) -> EmailFinderResult:
        """Find an email for a person and cache the result."""
        finder_result = self._client.find_email(domain, first_name, last_name)
        self._storage.create(
            f'finder:{domain}:{first_name}:{last_name}',
            finder_result,
        )
        return finder_result

    def search_domain(
        self,
        domain: str,
        limit: int = 10,
    ) -> DomainSearchResult:
        """Search emails by domain and cache the result."""
        domain_search_result = self._client.search_domain(domain, limit)
        self._storage.create(f'domain:{domain}', domain_search_result)
        return domain_search_result
