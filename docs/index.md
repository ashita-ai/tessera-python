# Tessera Python SDK

**Python SDK for Tessera - Data contract coordination for warehouses.**

The Tessera SDK provides a type-safe Python client for interacting with the [Tessera API](https://github.com/ashita-ai/tessera). It supports both synchronous and asynchronous operations.

## Why Use the SDK?

- **Type-safe** - Full Pydantic model support with IDE autocompletion
- **Sync and async** - Choose the client that fits your use case
- **Error handling** - Typed exceptions for different error scenarios
- **Simple configuration** - Environment variables or explicit config

## Quick Example

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
```

## Getting Started

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Installation**

    ---

    Install the SDK via pip or uv

    [:octicons-arrow-right-24: Installation](getting-started/installation.md)

-   :material-clock-fast:{ .lg .middle } **Quickstart**

    ---

    Get up and running in 5 minutes

    [:octicons-arrow-right-24: Quickstart](getting-started/quickstart.md)

-   :material-cog:{ .lg .middle } **Configuration**

    ---

    Configure authentication and options

    [:octicons-arrow-right-24: Configuration](getting-started/configuration.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete client and model documentation

    [:octicons-arrow-right-24: API Reference](api/client.md)

</div>

## Resources

| Resource | Description |
|----------|-------------|
| `client.teams` | Team management |
| `client.assets` | Asset and contract management |
| `client.contracts` | Contract lookup and comparison |
| `client.registrations` | Consumer registration |
| `client.proposals` | Breaking change proposals |

## Related

- [Tessera Server](https://github.com/ashita-ai/tessera) - The Tessera API server
- [Tessera Documentation](https://ashita-ai.github.io/tessera) - Full server documentation
- [PyPI Package](https://pypi.org/project/tessera-sdk/) - Install via pip
