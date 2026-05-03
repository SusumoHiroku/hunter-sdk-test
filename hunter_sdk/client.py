"""Endpoint-specific HTTP clients for the Hunter API v2."""

import json
from typing import Any, Mapping

import httpx

from hunter_sdk.exceptions import HunterAPIError, HunterRequestError, HunterResponseError
from hunter_sdk.models import DomainSearchResult, EmailFinderResult, EmailVerificationResult

_DEFAULT_BASE_URL: str = 'https://api.hunter.io/v2'
_DEFAULT_TIMEOUT: float = 10.0
_HTTP_OK: int = 200

_VERIFY_ENDPOINT: str = '/email-verifier'
_FINDER_ENDPOINT: str = '/email-finder'
_DOMAIN_SEARCH_ENDPOINT: str = '/domain-search'

_DATA_KEY: str = 'data'
_DOMAIN_KEY: str = 'domain'
_EMAIL_KEY: str = 'email'
_LIMIT_KEY: str = 'limit'


class _BaseHunterClient:
    """Shared HTTP transport for Hunter API endpoint clients."""

    def __init__(
        self,
        api_key: str,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize with credentials and connection settings."""
        self._api_key = api_key
        self._base_url = base_url.rstrip('/')
        self._timeout = timeout

    def _get(
        self,
        path: str,
        query_params: dict[str, Any],
    ) -> Mapping[str, Any]:
        """Execute a GET request and return the parsed JSON payload."""
        merged_params = {**query_params, 'api_key': self._api_key}
        try:
            response = httpx.get(
                f'{self._base_url}{path}',
                params=merged_params,
                timeout=self._timeout,
            )
        except httpx.RequestError as exc:
            raise HunterRequestError(str(exc)) from exc

        if response.status_code != _HTTP_OK:
            raise HunterAPIError(response.status_code, response.text)

        try:
            response_payload: Mapping[str, Any] = response.json()
        except json.JSONDecodeError as exc:
            raise HunterResponseError('Invalid JSON response') from exc

        return response_payload


class EmailVerificationClient(_BaseHunterClient):
    """Client for the Hunter email verifier endpoint."""

    def verify(self, email: str) -> EmailVerificationResult:
        """Verify a single email address and return the structured result."""
        payload_data: Mapping[str, Any] = self._get(
            _VERIFY_ENDPOINT, {_EMAIL_KEY: email},
        ).get(_DATA_KEY, {})
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


class EmailFinderClient(_BaseHunterClient):
    """Client for the Hunter email finder endpoint."""

    def find(
        self,
        domain: str,
        first_name: str,
        last_name: str,
    ) -> EmailFinderResult:
        """Find an email address for a person at the given domain."""
        payload_data: Mapping[str, Any] = self._get(
            _FINDER_ENDPOINT,
            {_DOMAIN_KEY: domain, 'first_name': first_name, 'last_name': last_name},
        ).get(_DATA_KEY, {})
        return EmailFinderResult(
            email=payload_data.get(_EMAIL_KEY, ''),
            score=payload_data.get('score', 0),
            domain=payload_data.get(_DOMAIN_KEY, ''),
            first_name=payload_data.get('first_name', ''),
            last_name=payload_data.get('last_name', ''),
            position=payload_data.get('position', ''),
            sources=list(payload_data.get('sources', [])),
        )


class DomainSearchClient(_BaseHunterClient):
    """Client for the Hunter domain search endpoint."""

    def search(self, domain: str, limit: int = 10) -> DomainSearchResult:
        """Return a list of email addresses found for the given domain."""
        payload_data: Mapping[str, Any] = self._get(
            _DOMAIN_SEARCH_ENDPOINT,
            {_DOMAIN_KEY: domain, _LIMIT_KEY: limit},
        ).get(_DATA_KEY, {})
        return DomainSearchResult(
            domain=payload_data.get(_DOMAIN_KEY, ''),
            organization=payload_data.get('organization', ''),
            total=payload_data.get('total', 0),
            emails=list(payload_data.get('emails', [])),
        )
