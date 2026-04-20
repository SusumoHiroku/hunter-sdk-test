from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class EmailVerificationResult:
    email: str
    status: str
    score: int
    regexp: bool
    gibberish: bool
    disposable: bool
    webmail: bool
    mx_records: bool
    smtp_server: bool
    smtp_check: bool
    accept_all: bool
    block: bool
    sources: list[Mapping[str, Any]]


@dataclass(frozen=True)
class EmailFinderResult:
    email: str
    score: int
    domain: str
    first_name: str
    last_name: str
    position: str
    sources: list[Mapping[str, Any]]


@dataclass(frozen=True)
class DomainSearchResult:
    domain: str
    organization: str
    total: int
    emails: list[Mapping[str, Any]]
