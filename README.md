# Hunter SDK

A test assignment project. Mini Python SDK for [Hunter.io API v2](https://hunter.io/api-documentation/v2).

Built with clean architecture in mind: separated client, service, storage, models, and exceptions layers.

## What's implemented

- Email verification via `/email-verifier`
- Email finder via `/email-finder`
- Domain search via `/domain-search`
- In-memory CRUD storage
- Full mypy strict typing
- flake8 + wemake-python-styleguide compatible code

## Project structure

```
sdk-test/
  main.py          # demo entrypoint
  requirements.txt
  setup.cfg        # mypy + flake8 config
  hunter_sdk/
    client.py      # HTTP layer
    service.py     # orchestration
    storage.py     # in-memory storage
    models.py      # dataclass models
    exceptions.py  # exception hierarchy
```

## Install

```bash
pip install -r requirements.txt
```

## Set API key

```bash
export HUNTER_API_KEY=your_api_key_here
```

## Run demo

```bash
python main.py
```

## Check types

```bash
mypy hunter_sdk main.py
```

## Check style

```bash
flake8 hunter_sdk main.py
```
