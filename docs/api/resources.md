# Resources

API resources available on the client.

## TeamsResource

Manage teams in Tessera.

### Methods

#### list() -> List[Team]

List all teams.

```python
teams = client.teams.list()
for team in teams:
    print(f"{team.name}: {team.id}")
```

#### get(team_id: str) -> Team

Get a team by ID.

```python
team = client.teams.get("team-uuid")
print(team.name)
```

#### create(name: str, description: str | None = None) -> Team

Create a new team.

```python
team = client.teams.create(
    name="data-platform",
    description="Data platform team"
)
```

#### delete(team_id: str, force: bool = False) -> None

Soft delete a team. Use `force=True` if the team still owns assets.

```python
client.teams.delete("team-uuid", force=True)
```

#### restore(team_id: str) -> Team

Restore a soft-deleted team.

```python
restored = client.teams.restore("team-uuid")
```

#### reassign_assets(team_id: str, target_team_id: str, asset_ids: list[str] | None = None) -> dict

Reassign assets to another team before deletion.

```python
client.teams.reassign_assets(
    team_id="team-uuid",
    target_team_id="target-team-uuid",
    asset_ids=["asset-id-1", "asset-id-2"],
)
```

---

## AssetsResource

Manage assets and their contracts.

### Methods

#### list(team_id: str | None = None) -> List[Asset]

List assets, optionally filtered by team.

```python
# All assets
assets = client.assets.list()

# Assets owned by a team
assets = client.assets.list(team_id="team-uuid")
```

#### get(asset_id: str) -> Asset

Get an asset by ID.

```python
asset = client.assets.get("asset-uuid")
```

#### create(fqn: str, owner_team_id: str, description: str | None = None) -> Asset

Create a new asset.

```python
asset = client.assets.create(
    fqn="warehouse.analytics.dim_customers",
    owner_team_id="team-uuid",
    description="Customer dimension table"
)
```

#### delete(asset_id: str) -> None

Delete an asset.

```python
client.assets.delete("asset-uuid")
```

#### publish_contract(asset_id: str, schema: dict, version: str, compatibility_mode: str = "backward", force: bool = False) -> PublishResult

Publish a new contract for an asset.

```python
result = client.assets.publish_contract(
    asset_id="asset-uuid",
    schema={
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"}
        },
        "required": ["id"]
    },
    version="1.0.0",
    compatibility_mode="backward"
)

if result.published:
    print(f"Published: {result.contract.version}")
else:
    print(f"Breaking change, proposal: {result.proposal.id}")
```

#### check_impact(asset_id: str, proposed_schema: dict) -> ImpactResult

Check the impact of proposed schema changes.

```python
impact = client.assets.check_impact(
    asset_id="asset-uuid",
    proposed_schema={"type": "object", "properties": {...}}
)

if impact.safe_to_publish:
    print("No breaking changes")
else:
    print(f"Breaking changes: {impact.breaking_changes}")
    print(f"Affected consumers: {len(impact.affected_registrations)}")
```

---

## ContractsResource

Look up and compare contracts.

### Methods

#### get(contract_id: str) -> Contract

Get a contract by ID.

```python
contract = client.contracts.get("contract-uuid")
print(f"Version: {contract.version}")
print(f"Schema: {contract.schema}")
```

#### list(asset_id: str | None = None) -> List[Contract]

List contracts, optionally filtered by asset.

```python
# All contracts for an asset
contracts = client.contracts.list(asset_id="asset-uuid")
```

#### compare(contract_id: str, other_contract_id: str) -> CompareResult

Compare two contracts.

```python
result = client.contracts.compare(
    contract_id="contract-1-uuid",
    other_contract_id="contract-2-uuid"
)

print(f"Compatible: {result.compatible}")
print(f"Changes: {result.changes}")
```

---

## RegistrationsResource

Manage consumer registrations.

### Methods

#### list(contract_id: str | None = None, team_id: str | None = None) -> List[Registration]

List registrations.

```python
# All registrations for a contract
registrations = client.registrations.list(contract_id="contract-uuid")

# All registrations by a team
registrations = client.registrations.list(team_id="team-uuid")
```

#### get(registration_id: str) -> Registration

Get a registration by ID.

```python
registration = client.registrations.get("registration-uuid")
```

#### create(contract_id: str, consumer_team_id: str) -> Registration

Register as a consumer of a contract.

```python
registration = client.registrations.create(
    contract_id="contract-uuid",
    consumer_team_id="my-team-uuid"
)
```

#### delete(registration_id: str) -> None

Unregister from a contract.

```python
client.registrations.delete("registration-uuid")
```

---

## ProposalsResource

Manage breaking change proposals.

### Methods

#### list(status: str | None = None) -> List[Proposal]

List proposals.

```python
# All pending proposals
proposals = client.proposals.list(status="pending")
```

#### get(proposal_id: str) -> Proposal

Get a proposal by ID.

```python
proposal = client.proposals.get("proposal-uuid")
print(f"Status: {proposal.status}")
print(f"Breaking changes: {proposal.breaking_changes}")
```

#### acknowledge(proposal_id: str, team_id: str, accepted: bool, comment: str | None = None) -> Acknowledgment

Acknowledge a breaking change proposal.

```python
# Accept the breaking change
ack = client.proposals.acknowledge(
    proposal_id="proposal-uuid",
    team_id="my-team-uuid",
    accepted=True,
    comment="We've updated our downstream models"
)

# Reject the breaking change
ack = client.proposals.acknowledge(
    proposal_id="proposal-uuid",
    team_id="my-team-uuid",
    accepted=False,
    comment="This would break our dashboard"
)
```
