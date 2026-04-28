"""HTTP client for the Hunter API v2."""

import json
from typing import (
    Any,
    Mapping,
)

import httpx

from hunter_sdk.exceptions import (
    HunterAPIError,
    HunterRequestError,
    HunterResponseError,
)
from hunter_sdk.models import (
    DomainSearchResult,
    EmailFinderResult,
    EmailVerificationResult,
)

_DEFAULT_BASE_URL: str = 'https://api.hunter.io/v2'
_DEFAULT_TIMEOUT: float = 10.0

_VERIFY_ENDPOINT: str = '/email-verifier'
_FINDER_ENDPOINT: str = '/email-finder'
_DOMAIN_SEARCH_ENDPOINT: str = '/domain-search'

_DATA_KEY: str = 'data'
_DOMAIN_KEY: str = 'domain'
_EMAIL_KEY: str = 'email'
_LIMIT_KEY: str = 'limit'


class HunterClient:
    """HTTP client for the Hunter API v2."""

    def __init__(
        self,
        api_key: str,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the client with credentials and connection settings."""
        self._api_key = api_key
        self._base_url = base_url.rstrip('/')
        self._timeout = timeout

    def verify_email(self, email: str) -> EmailVerificationResult:
        """Verify single email address via email verifier."""
        response_payload = self._get(_VERIFY_ENDPOINT, {_EMAIL_KEY: email})
        payload_data: Mapping[str, Any] = response_payload.get(_DATA_KEY, {})
        return EmailVerificationResult(
            email=payload_data.get(_EMAIL_KEY, ''),
            status=payload_data.get('status', ''),
            score=payload_data.get('score', 0),
            is_regexp=payload_data.get('regexp', False),
            is_gibberish=payload_data.get('gibberish', False),
            is_disposable=payload_data.get('disposable', False),
            is_webmail=payload_data.get('webmail', False),
            has_mx_records=payload_data.get('mx_records', False),
            has_smtp_server=payload_data.get('smtp_server', False),
            is_smtp_check_passed=payload_data.get('smtp_check', False),
            is_accept_all=payload_data.get('accept_all', False),
            is_blocked=payload_data.get('block', False),
            sources=list(payload_data.get('sources', [])),
        )

    def find_email(
        self,
        domain: str,
        first_name: str,
        last_name: str,
    ) -> EmailFinderResult:
        """Find an email address for a person at a given domain."""
        query_params: dict[str, Any] = {
            _DOMAIN_KEY: domain,
            'first_name': first_name,
            'last_name': last_name,
        }
        response_payload = self._get(_FINDER_ENDPOINT, query_params)
        payload_data: Mapping[str, Any] = response_payload.get(_DATA_KEY, {})
        return EmailFinderResult(
            email=payload_data.get(_EMAIL_KEY, ''),
            score=payload_data.get('score', 0),
            domain=payload_data.get(_DOMAIN_KEY, ''),
            first_name=payload_data.get('first_name', ''),
            last_name=payload_data.get('last_name', ''),
            position=payload_data.get('position', ''),
            sources=list(payload_data.get('sources', [])),
        )

    def search_domain(
        self,
        domain: str,
        limit: int = 10,
    ) -> DomainSearchResult:
        """Return list of email addresses found for a domain."""
        query_params: dict[str, Any] = {
            _DOMAIN_KEY: domain,
            _LIMIT_KEY: limit,
        }
        response_payload = self._get(_DOMAIN_SEARCH_ENDPOINT, query_params)
        payload_data: Mapping[str, Any] = response_payload.get(_DATA_KEY, {})
        return DomainSearchResult(
            domain=payload_data.get(_DOMAIN_KEY, ''),
            organization=payload_data.get('organization', ''),
            total=payload_data.get('total', 0),
            emails=list(payload_data.get('emails', [])),
        )

    def _get(
        self,
        path: str,
        query_params: dict[str, Any],
    ) -> Mapping[str, Any]:
        """Execute GET request and return the parsed JSON payload."""
        merged_params = {**query_params, 'api_key': self._api_key}
        try:
            response = httpx.get(
                f'{self._base_url}{path}',
                params=merged_params,
                timeout=self._timeout,
            )
        except httpx.RequestError as exc:
            raise HunterRequestError(str(exc)) from exc

        if response.status_code != 200:  # noqa: WPS432
            raise HunterAPIError(response.status_code, response.text)

        try:
            response_payload: Mapping[str, Any] = response.json()
        except json.JSONDecodeError as exc:
            raise HunterResponseError('Invalid JSON response') from exc

        return response_payload
