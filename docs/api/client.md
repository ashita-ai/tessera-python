# Client

The main entry points for the Tessera SDK.

## TesseraClient

Synchronous client for the Tessera API.

```python
from tessera_sdk import TesseraClient

client = TesseraClient(
    base_url="http://localhost:8000",
    api_key="optional-api-key",
    timeout=30.0
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_url` | `str` | `TESSERA_URL` env var or `http://localhost:8000` | Base URL for the Tessera API |
| `api_key` | `str \| None` | `TESSERA_API_KEY` env var | API key for authentication |
| `timeout` | `float` | `30.0` | Request timeout in seconds |
| `http_client` | `httpx.Client \| None` | `None` | Custom httpx client |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `teams` | `TeamsResource` | Team management |
| `assets` | `AssetsResource` | Asset and contract management |
| `contracts` | `ContractsResource` | Contract lookup |
| `registrations` | `RegistrationsResource` | Consumer registration |
| `proposals` | `ProposalsResource` | Breaking change proposals |

### Context Manager

```python
with TesseraClient() as client:
    teams = client.teams.list()
# Client is automatically closed
```

### Methods

#### close()

Close the HTTP client and release resources.

```python
client = TesseraClient()
try:
    teams = client.teams.list()
finally:
    client.close()
```

---

## AsyncTesseraClient

Asynchronous client for the Tessera API.

```python
from tessera_sdk import AsyncTesseraClient

client = AsyncTesseraClient(
    base_url="http://localhost:8000",
    api_key="optional-api-key",
    timeout=30.0
)
```

### Parameters

Same as `TesseraClient`.

### Properties

Same as `TesseraClient`, but all methods are async.

### Async Context Manager

```python
async with AsyncTesseraClient() as client:
    teams = await client.teams.list()
# Client is automatically closed
```

### Methods

#### async close()

Close the HTTP client and release resources.

```python
client = AsyncTesseraClient()
try:
    teams = await client.teams.list()
finally:
    await client.close()
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TESSERA_URL` | Base URL for the API | `http://localhost:8000` |
| `TESSERA_API_KEY` | API key for authentication | None |

---

## Examples

### Basic Usage

```python
from tessera_sdk import TesseraClient

# Simple connection
client = TesseraClient(base_url="http://localhost:8000")

# List all teams
teams = client.teams.list()
for team in teams:
    print(f"Team: {team.name}")
```

### With Authentication

```python
client = TesseraClient(
    base_url="http://localhost:8000",
    api_key="your-api-key"
)
```

### Custom HTTP Client

```python
import httpx

custom_client = httpx.Client(
    timeout=60.0,
    headers={"X-Custom-Header": "value"},
    verify=False  # Disable SSL verification
)

client = TesseraClient(
    base_url="http://localhost:8000",
    http_client=custom_client
)
```

### Async with FastAPI

```python
from fastapi import FastAPI, Depends
from tessera_sdk import AsyncTesseraClient

app = FastAPI()

async def get_client():
    async with AsyncTesseraClient() as client:
        yield client

@app.get("/teams")
async def list_teams(client: AsyncTesseraClient = Depends(get_client)):
    return await client.teams.list()
```
