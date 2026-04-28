"""Demo script for the Hunter sdk."""

import os
import sys

from hunter_sdk.client import HunterClient
from hunter_sdk.exceptions import HunterSDKError
from hunter_sdk.models import EmailVerificationResult
from hunter_sdk.service import HunterService
from hunter_sdk.storage import InMemoryStorage

_DEMO_EMAIL: str = 'tonyplink@gmail.com'


def _get_api_key() -> str:
    """Read the Hunter API key from the environment."""
    api_key = os.getenv('HUNTER_API_KEY')
    if api_key is None:
        raise RuntimeError('HUNTER_API_KEY environment variable is not set')
    return api_key


def _build_service() -> HunterService:
    """Assemble the service with its dependencies."""
    api_key = _get_api_key()
    client = HunterClient(api_key=api_key)
    storage = InMemoryStorage()
    return HunterService(client=client, storage=storage)


def _run_demo() -> EmailVerificationResult:
    """Run the demo verification and return the result."""
    service = _build_service()
    return service.verify_email(email=_DEMO_EMAIL)


def _print_result(verification_result: EmailVerificationResult) -> None:
    """Print key fields from the verification result to stdout."""
    sys.stdout.write(f'Email:      {verification_result.email}\n')
    sys.stdout.write(f'Status:     {verification_result.status}\n')
    sys.stdout.write(f'Score:      {verification_result.score}\n')
    sys.stdout.write(f'Disposable: {verification_result.is_disposable}\n')
    sys.stdout.write(f'Webmail:    {verification_result.is_webmail}\n')
    sys.stdout.write(f'Stored:     {verification_result}\n')


def main() -> None:
    """Entry point for the demo script."""
    try:
        verification_result = _run_demo()
    except HunterSDKError as exc:
        sys.stderr.write(f'SDK error: {exc}\n')
        sys.exit(1)
    except RuntimeError as exc:
        sys.stderr.write(f'{exc}\n')
        sys.exit(1)

    _print_result(verification_result)


if __name__ == '__main__':
    main()
