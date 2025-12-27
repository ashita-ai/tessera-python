# Models

Pydantic models returned by the SDK.

## Team

Represents a team that owns assets or consumes contracts.

```python
class Team:
    id: UUID
    name: str
    description: str | None
    created_at: datetime
```

**Example:**

```python
team = client.teams.get("team-uuid")
print(team.id)          # UUID
print(team.name)        # "data-platform"
print(team.description) # "Data platform team"
print(team.created_at)  # datetime
```

---

## Asset

Represents a data asset (table, view, model).

```python
class Asset:
    id: UUID
    fqn: str
    owner_team_id: UUID
    description: str | None
    created_at: datetime
    current_contract_id: UUID | None
```

**Example:**

```python
asset = client.assets.get("asset-uuid")
print(asset.fqn)                  # "warehouse.analytics.dim_customers"
print(asset.owner_team_id)        # UUID
print(asset.current_contract_id)  # UUID of active contract
```

---

## Contract

Represents a data contract defining the schema.

```python
class Contract:
    id: UUID
    asset_id: UUID
    version: str
    schema: dict
    compatibility_mode: str
    status: str  # "active", "deprecated", "superseded"
    created_at: datetime
    deprecated_at: datetime | None
```

**Example:**

```python
contract = client.contracts.get("contract-uuid")
print(contract.version)            # "1.0.0"
print(contract.schema)             # {"type": "object", ...}
print(contract.compatibility_mode) # "backward"
print(contract.status)             # "active"
```

---

## Registration

Represents a team's registration to consume a contract.

```python
class Registration:
    id: UUID
    contract_id: UUID
    consumer_team_id: UUID
    created_at: datetime
```

**Example:**

```python
registration = client.registrations.get("registration-uuid")
print(registration.contract_id)       # UUID
print(registration.consumer_team_id)  # UUID
```

---

## Proposal

Represents a proposal for a breaking change.

```python
class Proposal:
    id: UUID
    asset_id: UUID
    proposed_schema: dict
    proposed_version: str
    breaking_changes: list[str]
    status: str  # "pending", "approved", "rejected", "expired"
    created_at: datetime
    resolved_at: datetime | None
```

**Example:**

```python
proposal = client.proposals.get("proposal-uuid")
print(proposal.status)           # "pending"
print(proposal.breaking_changes) # ["Removed required field 'email'"]
```

---

## Acknowledgment

Represents a team's acknowledgment of a proposal.

```python
class Acknowledgment:
    id: UUID
    proposal_id: UUID
    team_id: UUID
    accepted: bool
    comment: str | None
    created_at: datetime
```

---

## PublishResult

Returned by `assets.publish_contract()`.

```python
class PublishResult:
    published: bool
    contract: Contract | None   # Set if published=True
    proposal: Proposal | None   # Set if published=False (breaking change)
```

**Example:**

```python
result = client.assets.publish_contract(...)

if result.published:
    print(f"Published contract: {result.contract.id}")
else:
    print(f"Breaking change, proposal: {result.proposal.id}")
```

---

## ImpactResult

Returned by `assets.check_impact()`.

```python
class ImpactResult:
    safe_to_publish: bool
    breaking_changes: list[str]
    affected_registrations: list[Registration]
```

**Example:**

```python
impact = client.assets.check_impact(
    asset_id="asset-uuid",
    proposed_schema={...}
)

if not impact.safe_to_publish:
    print("Breaking changes detected:")
    for change in impact.breaking_changes:
        print(f"  - {change}")

    print("Affected consumers:")
    for reg in impact.affected_registrations:
        print(f"  - Team {reg.consumer_team_id}")
```

---

## CompareResult

Returned by `contracts.compare()`.

```python
class CompareResult:
    compatible: bool
    changes: list[str]
```

**Example:**

```python
result = client.contracts.compare(
    contract_id="v1-uuid",
    other_contract_id="v2-uuid"
)

if result.compatible:
    print("Contracts are compatible")
else:
    print("Incompatible changes:")
    for change in result.changes:
        print(f"  - {change}")
```
