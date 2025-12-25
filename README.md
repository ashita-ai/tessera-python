<p align="center">
  <img src="https://raw.githubusercontent.com/ashita-ai/tessera-python/main/assets/logo.png" alt="Tessera" width="200">
</p>

<h1 align="center">Tessera Python SDK</h1>

<p align="center">
  <strong>Python SDK for <a href="https://github.com/ashita-ai/tessera">Tessera</a> - Data Contract Coordination</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/tessera-sdk/"><img src="https://img.shields.io/pypi/v/tessera-sdk" alt="PyPI"></a>
  <a href="https://pypi.org/project/tessera-sdk/"><img src="https://img.shields.io/pypi/pyversions/tessera-sdk" alt="Python"></a>
</p>

---

Tessera coordinates data contracts between producers and consumers. Producers publish schemas, consumers register dependencies, and breaking changes require acknowledgment before deployment.

**This SDK provides a Python client for the Tessera API.**

## Installation

```bash
pip install tessera-sdk
```

Or with uv:

```bash
uv add tessera-sdk
```

## Quick Start

```python
from tessera_sdk import TesseraClient

client = TesseraClient(base_url="http://localhost:8000")

# Create a team
team = client.teams.create(name="data-platform")

# Create an asset
asset = client.assets.create(
    fqn="warehouse.analytics.dim_customers",
    owner_team_id=team.id
)

# Publish a contract
result = client.assets.publish_contract(
    asset_id=asset.id,
    schema={
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"}
        }
    },
    version="1.0.0"
)

# Check impact before making changes
impact = client.assets.check_impact(
    asset_id=asset.id,
    proposed_schema={
        "type": "object",
        "properties": {
            "id": {"type": "string"},  # Changed type!
            "name": {"type": "string"}
        }
    }
)

if not impact.safe_to_publish:
    print(f"Breaking changes detected: {impact.breaking_changes}")
```

## Features

- **Sync and async clients** - Use `TesseraClient` or `AsyncTesseraClient`
- **Type-safe** - Full Pydantic model support
- **Error handling** - Typed exceptions for API errors
- **Flexible configuration** - Environment variables or explicit config

## Async Support

```python
import asyncio
from tessera_sdk import AsyncTesseraClient

async def main():
    async with AsyncTesseraClient() as client:
        team = await client.teams.create(name="data-platform")
        print(f"Created team: {team.name}")

asyncio.run(main())
```

## Airflow Integration

```python
from airflow.decorators import task
from tessera_sdk import TesseraClient

@task
def validate_schema():
    client = TesseraClient()
    impact = client.assets.check_impact(
        asset_id="your-asset-id",
        proposed_schema=load_schema("./schema.json")
    )
    if not impact.safe_to_publish:
        raise ValueError(f"Breaking changes: {impact.breaking_changes}")

@task
def publish_contract():
    client = TesseraClient()
    client.assets.publish_contract(
        asset_id="your-asset-id",
        schema=load_schema("./schema.json"),
        version=get_version()
    )
```

## API Reference

### TesseraClient

The main client class with the following resources:

| Resource | Description |
|----------|-------------|
| `client.teams` | Team management |
| `client.assets` | Asset and contract management |
| `client.contracts` | Contract lookup and comparison |
| `client.registrations` | Consumer registration |
| `client.proposals` | Breaking change proposals |

### Configuration

```python
# Explicit URL
client = TesseraClient(base_url="http://localhost:8000")

# Environment variable (TESSERA_URL)
client = TesseraClient()  # Uses TESSERA_URL or defaults to localhost:8000

# With authentication
client = TesseraClient(
    base_url="http://localhost:8000",
    api_key="your-api-key",
    timeout=30.0
)
```

## Error Handling

```python
from tessera_sdk import TesseraClient, NotFoundError, ValidationError

client = TesseraClient()

try:
    team = client.teams.get("non-existent-id")
except NotFoundError:
    print("Team not found")
except ValidationError as e:
    print(f"Validation error: {e.message}")
```

## Requirements

- Python 3.10+
- httpx >= 0.25.0
- pydantic >= 2.0.0

## Related

- [Tessera Server](https://github.com/ashita-ai/tessera) - The Tessera API server
- [Tessera Documentation](https://ashita-ai.github.io/tessera) - Full documentation

