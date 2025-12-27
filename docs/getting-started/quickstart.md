# Quickstart

This guide will get you up and running with the Tessera SDK in 5 minutes.

## Prerequisites

1. A running Tessera server (see [Tessera docs](https://ashita-ai.github.io/tessera))
2. Python 3.10+
3. The SDK installed: `pip install tessera-sdk`

## Basic Usage

### Create a client

```python
from tessera_sdk import TesseraClient

# Connect to local server
client = TesseraClient(base_url="http://localhost:8000")

# Or with authentication
client = TesseraClient(
    base_url="http://localhost:8000",
    api_key="your-api-key"
)
```

### Create a team

```python
team = client.teams.create(name="data-platform")
print(f"Created team: {team.id}")
```

### Create an asset

```python
asset = client.assets.create(
    fqn="warehouse.analytics.dim_customers",
    owner_team_id=team.id,
    description="Customer dimension table"
)
print(f"Created asset: {asset.id}")
```

### Publish a contract

```python
result = client.assets.publish_contract(
    asset_id=asset.id,
    schema={
        "type": "object",
        "properties": {
            "customer_id": {"type": "integer"},
            "email": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"}
        },
        "required": ["customer_id", "email"]
    },
    version="1.0.0"
)

if result.published:
    print(f"Published contract v{result.contract.version}")
else:
    print(f"Breaking change detected, proposal created: {result.proposal.id}")
```

### Check impact before changes

```python
impact = client.assets.check_impact(
    asset_id=asset.id,
    proposed_schema={
        "type": "object",
        "properties": {
            "customer_id": {"type": "string"},  # Type changed!
            "email": {"type": "string"}
        }
    }
)

if impact.safe_to_publish:
    print("Safe to publish - no breaking changes")
else:
    print(f"Breaking changes: {impact.breaking_changes}")
    print(f"Affected consumers: {len(impact.affected_registrations)}")
```

### Register as a consumer

```python
registration = client.registrations.create(
    contract_id=contract.id,
    consumer_team_id=my_team.id
)
print(f"Registered for contract: {registration.id}")
```

## Complete Example

```python
from tessera_sdk import TesseraClient

def main():
    client = TesseraClient(base_url="http://localhost:8000")

    # Setup
    team = client.teams.create(name="analytics-team")
    asset = client.assets.create(
        fqn="analytics.core.users",
        owner_team_id=team.id
    )

    # Publish initial contract
    result = client.assets.publish_contract(
        asset_id=asset.id,
        schema={
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
                "email": {"type": "string"}
            },
            "required": ["user_id"]
        },
        version="1.0.0"
    )
    print(f"Published: {result.contract.version}")

    # Check impact of adding a required field
    impact = client.assets.check_impact(
        asset_id=asset.id,
        proposed_schema={
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
                "email": {"type": "string"},
                "name": {"type": "string"}  # New field
            },
            "required": ["user_id", "name"]  # name is now required!
        }
    )

    print(f"Safe to publish: {impact.safe_to_publish}")
    print(f"Breaking changes: {impact.breaking_changes}")

if __name__ == "__main__":
    main()
```

## Next steps

- [Configuration](configuration.md) - Advanced configuration options
- [Async Usage](../guides/async.md) - Use the async client
- [Error Handling](../guides/error-handling.md) - Handle errors gracefully
