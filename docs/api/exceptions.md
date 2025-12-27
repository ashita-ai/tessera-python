# Exceptions

Typed exceptions for error handling.

## Exception Hierarchy

```
TesseraError
├── TesseraAPIError
│   ├── NotFoundError
│   ├── ValidationError
│   ├── ConflictError
│   └── AuthenticationError
└── TesseraConnectionError
```

---

## TesseraError

Base exception for all SDK errors.

```python
from tessera_sdk.exceptions import TesseraError

try:
    asset = client.assets.get("asset-uuid")
except TesseraError as e:
    print(f"Tessera error: {e}")
```

---

## TesseraAPIError

Base exception for API errors. Contains HTTP status and details.

```python
from tessera_sdk.exceptions import TesseraAPIError

try:
    asset = client.assets.get("asset-uuid")
except TesseraAPIError as e:
    print(e.status_code)  # HTTP status code (e.g., 404)
    print(e.message)      # Error message
    print(e.details)      # Additional details (if any)
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `status_code` | `int` | HTTP status code |
| `message` | `str` | Error message |
| `details` | `dict \| None` | Additional error details |

---

## NotFoundError

Raised when a resource is not found (HTTP 404).

```python
from tessera_sdk.exceptions import NotFoundError

try:
    asset = client.assets.get("non-existent-id")
except NotFoundError as e:
    print(f"Asset not found: {e.message}")
```

---

## ValidationError

Raised when request validation fails (HTTP 422).

```python
from tessera_sdk.exceptions import ValidationError

try:
    asset = client.assets.create(
        fqn="",  # Invalid: empty FQN
        owner_team_id="team-uuid"
    )
except ValidationError as e:
    print(f"Validation failed: {e.message}")
    print(f"Details: {e.details}")
```

---

## ConflictError

Raised when there's a resource conflict (HTTP 409).

```python
from tessera_sdk.exceptions import ConflictError

try:
    team = client.teams.create(name="existing-team")
except ConflictError as e:
    print(f"Conflict: {e.message}")
```

---

## AuthenticationError

Raised for authentication/authorization failures (HTTP 401/403).

```python
from tessera_sdk.exceptions import AuthenticationError

try:
    client = TesseraClient(api_key="invalid-key")
    teams = client.teams.list()
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
```

---

## TesseraConnectionError

Raised when the client cannot connect to the server.

```python
from tessera_sdk.exceptions import TesseraConnectionError

try:
    client = TesseraClient(base_url="http://unreachable:8000")
    teams = client.teams.list()
except TesseraConnectionError as e:
    print(f"Connection failed: {e}")
```

---

## Usage Patterns

### Catch Specific First

```python
from tessera_sdk.exceptions import (
    NotFoundError,
    ValidationError,
    TesseraAPIError,
    TesseraError,
)

try:
    result = client.assets.publish_contract(...)
except NotFoundError:
    print("Asset not found")
except ValidationError as e:
    print(f"Invalid request: {e.details}")
except TesseraAPIError as e:
    print(f"API error {e.status_code}: {e.message}")
except TesseraError as e:
    print(f"SDK error: {e}")
```

### Retry on Connection Errors

```python
import time
from tessera_sdk.exceptions import TesseraConnectionError

def with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except TesseraConnectionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Logging

```python
import logging
from tessera_sdk.exceptions import TesseraAPIError

logger = logging.getLogger(__name__)

try:
    asset = client.assets.get(asset_id)
except TesseraAPIError as e:
    logger.error(
        "API error",
        extra={
            "status_code": e.status_code,
            "message": e.message,
            "details": e.details,
        }
    )
    raise
```
