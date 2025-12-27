# Error Handling

The Tessera SDK provides typed exceptions for different error scenarios.

## Exception Hierarchy

```
TesseraError (base)
├── TesseraAPIError (API returned an error)
│   ├── NotFoundError (404)
│   ├── ValidationError (422)
│   ├── ConflictError (409)
│   └── AuthenticationError (401/403)
└── TesseraConnectionError (network issues)
```

## Basic Error Handling

```python
from tessera_sdk import TesseraClient
from tessera_sdk.exceptions import (
    TesseraError,
    NotFoundError,
    ValidationError,
    ConflictError,
)

client = TesseraClient()

try:
    asset = client.assets.get("non-existent-id")
except NotFoundError as e:
    print(f"Asset not found: {e.message}")
except TesseraError as e:
    print(f"Tessera error: {e}")
```

## Specific Exceptions

### NotFoundError

Raised when a resource doesn't exist (HTTP 404):

```python
from tessera_sdk.exceptions import NotFoundError

try:
    asset = client.assets.get(asset_id)
except NotFoundError:
    print("Asset does not exist")
```

### ValidationError

Raised when request data is invalid (HTTP 422):

```python
from tessera_sdk.exceptions import ValidationError

try:
    asset = client.assets.create(
        fqn="",  # Invalid: empty FQN
        owner_team_id=team.id
    )
except ValidationError as e:
    print(f"Validation failed: {e.message}")
    print(f"Details: {e.details}")
```

### ConflictError

Raised when there's a conflict (HTTP 409):

```python
from tessera_sdk.exceptions import ConflictError

try:
    team = client.teams.create(name="existing-team")
except ConflictError:
    print("Team already exists")
```

### AuthenticationError

Raised for authentication/authorization issues (HTTP 401/403):

```python
from tessera_sdk.exceptions import AuthenticationError

try:
    client = TesseraClient(api_key="invalid-key")
    teams = client.teams.list()
except AuthenticationError:
    print("Invalid API key")
```

### TesseraConnectionError

Raised for network issues:

```python
from tessera_sdk.exceptions import TesseraConnectionError

try:
    client = TesseraClient(base_url="http://unreachable:8000")
    teams = client.teams.list()
except TesseraConnectionError:
    print("Cannot connect to Tessera server")
```

## Error Properties

All API errors have these properties:

```python
try:
    asset = client.assets.get(asset_id)
except TesseraAPIError as e:
    print(e.status_code)  # HTTP status code
    print(e.message)      # Error message
    print(e.details)      # Additional details (if any)
```

## Retry Logic

For transient errors, implement retry logic:

```python
import time
from tessera_sdk.exceptions import TesseraConnectionError, TesseraAPIError

def with_retry(func, max_retries=3, delay=1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except TesseraConnectionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay * (2 ** attempt))  # Exponential backoff
        except TesseraAPIError as e:
            if e.status_code >= 500:  # Server error, retry
                if attempt == max_retries - 1:
                    raise
                time.sleep(delay)
            else:
                raise  # Client error, don't retry

# Usage
asset = with_retry(lambda: client.assets.get(asset_id))
```

## Async Error Handling

The same exceptions work with the async client:

```python
from tessera_sdk import AsyncTesseraClient
from tessera_sdk.exceptions import NotFoundError

async def get_asset_safe(client, asset_id):
    try:
        return await client.assets.get(asset_id)
    except NotFoundError:
        return None
```

## Best Practices

1. **Catch specific exceptions first**, then fall back to general ones:

```python
try:
    result = client.assets.publish_contract(...)
except ValidationError as e:
    # Handle validation issues
    pass
except ConflictError as e:
    # Handle conflicts
    pass
except TesseraAPIError as e:
    # Handle other API errors
    pass
except TesseraError as e:
    # Handle all Tessera errors
    pass
```

2. **Log error details** for debugging:

```python
import logging

logger = logging.getLogger(__name__)

try:
    asset = client.assets.get(asset_id)
except TesseraAPIError as e:
    logger.error(
        "Tessera API error",
        extra={
            "status_code": e.status_code,
            "message": e.message,
            "details": e.details,
        }
    )
    raise
```

3. **Use context managers** to ensure cleanup on errors:

```python
with TesseraClient() as client:
    # If an error occurs, the client is still properly closed
    asset = client.assets.get(asset_id)
```
