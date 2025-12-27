# Async Usage

The Tessera SDK provides an async client for use in asynchronous applications.

## AsyncTesseraClient

```python
from tessera_sdk import AsyncTesseraClient

async def main():
    client = AsyncTesseraClient(base_url="http://localhost:8000")

    # All methods are async
    teams = await client.teams.list()
    for team in teams:
        print(team.name)
```

## Context Manager

Always use the async context manager to ensure proper cleanup:

```python
async with AsyncTesseraClient() as client:
    teams = await client.teams.list()
```

## Complete Example

```python
import asyncio
from tessera_sdk import AsyncTesseraClient

async def setup_data_contracts():
    async with AsyncTesseraClient(base_url="http://localhost:8000") as client:
        # Create team
        team = await client.teams.create(name="data-platform")

        # Create asset
        asset = await client.assets.create(
            fqn="warehouse.analytics.dim_customers",
            owner_team_id=team.id,
            description="Customer dimension table"
        )

        # Publish contract
        result = await client.assets.publish_contract(
            asset_id=asset.id,
            schema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "integer"},
                    "email": {"type": "string"}
                },
                "required": ["customer_id"]
            },
            version="1.0.0"
        )

        print(f"Published contract: {result.contract.version}")
        return result

if __name__ == "__main__":
    asyncio.run(setup_data_contracts())
```

## Parallel Operations

Use `asyncio.gather` for parallel operations:

```python
async def check_multiple_assets(client, asset_ids):
    tasks = [
        client.assets.get(asset_id)
        for asset_id in asset_ids
    ]
    assets = await asyncio.gather(*tasks)
    return assets
```

## Integration with Async Frameworks

### FastAPI

```python
from fastapi import FastAPI, Depends
from tessera_sdk import AsyncTesseraClient

app = FastAPI()

async def get_tessera_client():
    async with AsyncTesseraClient() as client:
        yield client

@app.get("/assets/{asset_id}")
async def get_asset(asset_id: str, client: AsyncTesseraClient = Depends(get_tessera_client)):
    return await client.assets.get(asset_id)
```

### aiohttp

```python
import aiohttp
from tessera_sdk import AsyncTesseraClient

async def process_with_tessera():
    async with aiohttp.ClientSession() as http_session:
        async with AsyncTesseraClient() as tessera:
            # Use both clients
            assets = await tessera.assets.list()
            # Process assets...
```

## When to Use Async

Use `AsyncTesseraClient` when:

- Your application is already async (FastAPI, aiohttp, etc.)
- You need to make many concurrent API calls
- You want non-blocking I/O

Use `TesseraClient` (sync) when:

- Your application is synchronous
- You're writing scripts or CLI tools
- Simplicity is more important than concurrency
