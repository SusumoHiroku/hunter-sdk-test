from hunter_sdk.client import HunterClient
from hunter_sdk.models import (
    DomainSearchResult,
    EmailFinderResult,
    EmailVerificationResult,
)
from hunter_sdk.storage import InMemoryStorage


class HunterService:

    def __init__(
        self,
        client: HunterClient,
        storage: InMemoryStorage,
    ) -> None:
        self._client = client
        self._storage = storage

    def verify_email(self, email: str) -> EmailVerificationResult:
        verification_result = self._client.verify_email(email)
        self._storage.create(f"verify:{email}", verification_result)
        return verification_result

    def find_email(
        self,
        domain: str,
        first_name: str,
        last_name: str,
    ) -> EmailFinderResult:
        finder_result = self._client.find_email(domain, first_name, last_name)
        self._storage.create(
            f"finder:{domain}:{first_name}:{last_name}",
            finder_result,
        )
        return finder_result

    def search_domain(
        self,
        domain: str,
        limit: int = 10,
    ) -> DomainSearchResult:
        domain_search_result = self._client.search_domain(domain, limit)
        self._storage.create(f"domain:{domain}", domain_search_result)
        return domain_search_result
