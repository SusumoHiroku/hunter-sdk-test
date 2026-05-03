"""Dataclass models for Hunter API responses."""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class EmailVerificationResult:
    """Result of an email verification request."""

    email: str
    status: str
    score: int
    is_regexp: bool
    is_gibberish: bool
    is_disposable: bool
    is_webmail: bool
    has_mx_records: bool
    has_smtp_server: bool
    is_smtp_check_passed: bool
    is_accept_all: bool
    is_blocked: bool
    sources: list[Mapping[str, Any]]


@dataclass(frozen=True)
class EmailFinderResult:
    """Result of an email finder request."""

    email: str
    score: int
    domain: str
    first_name: str
    last_name: str
    position: str
    sources: list[Mapping[str, Any]]


@dataclass(frozen=True)
class DomainSearchResult:
    """Result of a domain search request."""

    domain: str
    organization: str
    total: int
    emails: list[Mapping[str, Any]]
