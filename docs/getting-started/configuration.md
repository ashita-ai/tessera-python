# Configuration

## Client Options

### Base URL

```python
# Explicit URL
client = TesseraClient(base_url="http://localhost:8000")

# From environment variable (TESSERA_URL)
client = TesseraClient()  # Uses TESSERA_URL or defaults to http://localhost:8000
```

### Authentication

```python
# With API key
client = TesseraClient(
    base_url="http://localhost:8000",
    api_key="your-api-key"
)

# From environment variable (TESSERA_API_KEY)
import os
os.environ["TESSERA_API_KEY"] = "your-api-key"
client = TesseraClient()
```

### Timeout

```python
# Custom timeout (seconds)
client = TesseraClient(
    base_url="http://localhost:8000",
    timeout=30.0  # Default is 30 seconds
)
```

### Custom HTTP Client

```python
import httpx

# Use a custom httpx client
custom_client = httpx.Client(
    timeout=60.0,
    headers={"X-Custom-Header": "value"}
)

client = TesseraClient(
    base_url="http://localhost:8000",
    http_client=custom_client
)
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TESSERA_URL` | Base URL for the Tessera API | `http://localhost:8000` |
| `TESSERA_API_KEY` | API key for authentication | None |

## Async Client

The async client accepts the same configuration options:

```python
from tessera_sdk import AsyncTesseraClient

client = AsyncTesseraClient(
    base_url="http://localhost:8000",
    api_key="your-api-key",
    timeout=30.0
)
```

## Context Manager

Both clients support context manager usage:

```python
# Sync
with TesseraClient() as client:
    teams = client.teams.list()

# Async
async with AsyncTesseraClient() as client:
    teams = await client.teams.list()
```

This ensures proper cleanup of HTTP connections.
