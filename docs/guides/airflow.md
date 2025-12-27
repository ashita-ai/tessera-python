# Airflow Integration

Use the Tessera SDK in Apache Airflow to integrate data contracts into your data pipelines.

## Installation

Install the SDK in your Airflow environment:

```bash
pip install tessera-sdk
```

## Basic Operator

Create a custom operator for Tessera operations:

```python
from airflow.models import BaseOperator
from tessera_sdk import TesseraClient

class TesseraPublishContractOperator(BaseOperator):
    """Publish a contract to Tessera."""

    def __init__(
        self,
        asset_id: str,
        schema: dict,
        version: str,
        tessera_url: str = "http://localhost:8000",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.asset_id = asset_id
        self.schema = schema
        self.version = version
        self.tessera_url = tessera_url

    def execute(self, context):
        client = TesseraClient(base_url=self.tessera_url)

        result = client.assets.publish_contract(
            asset_id=self.asset_id,
            schema=self.schema,
            version=self.version
        )

        if result.published:
            self.log.info(f"Published contract v{result.contract.version}")
            return {"contract_id": str(result.contract.id)}
        else:
            self.log.warning(f"Breaking change - proposal created: {result.proposal.id}")
            return {"proposal_id": str(result.proposal.id)}
```

## Impact Check Operator

Check impact before making changes:

```python
class TesseraImpactCheckOperator(BaseOperator):
    """Check impact of schema changes."""

    def __init__(
        self,
        asset_id: str,
        proposed_schema: dict,
        tessera_url: str = "http://localhost:8000",
        fail_on_breaking: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.asset_id = asset_id
        self.proposed_schema = proposed_schema
        self.tessera_url = tessera_url
        self.fail_on_breaking = fail_on_breaking

    def execute(self, context):
        client = TesseraClient(base_url=self.tessera_url)

        impact = client.assets.check_impact(
            asset_id=self.asset_id,
            proposed_schema=self.proposed_schema
        )

        if not impact.safe_to_publish and self.fail_on_breaking:
            raise AirflowException(
                f"Breaking changes detected: {impact.breaking_changes}"
            )

        return {
            "safe_to_publish": impact.safe_to_publish,
            "breaking_changes": impact.breaking_changes,
            "affected_consumers": len(impact.affected_registrations)
        }
```

## Example DAG

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from tessera_sdk import TesseraClient

def publish_contract(**context):
    client = TesseraClient(base_url="http://tessera:8000")

    result = client.assets.publish_contract(
        asset_id=context["params"]["asset_id"],
        schema=context["params"]["schema"],
        version=context["params"]["version"]
    )

    return {"published": result.published}

with DAG(
    "publish_data_contract",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    publish = PythonOperator(
        task_id="publish_contract",
        python_callable=publish_contract,
        params={
            "asset_id": "{{ var.value.asset_id }}",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                }
            },
            "version": "1.0.0"
        }
    )
```

## Using with dbt

Sync contracts after dbt runs:

```python
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.operators.python import PythonOperator

def sync_contracts_from_dbt(**context):
    """Sync contracts from dbt manifest after successful run."""
    client = TesseraClient(base_url="http://tessera:8000")

    # Read manifest from dbt artifacts
    manifest_path = "/path/to/target/manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)

    # Sync to Tessera
    result = client.sync.dbt(manifest=manifest, team_id="your-team-id")

    return {
        "synced_assets": result.synced_count,
        "errors": result.errors
    }

with DAG("dbt_with_tessera", ...):

    dbt_run = DbtCloudRunJobOperator(
        task_id="dbt_run",
        job_id=12345,
    )

    sync_contracts = PythonOperator(
        task_id="sync_contracts",
        python_callable=sync_contracts_from_dbt,
    )

    dbt_run >> sync_contracts
```

## Environment Configuration

Use Airflow Variables or Connections:

```python
from airflow.models import Variable

def get_tessera_client():
    return TesseraClient(
        base_url=Variable.get("tessera_url"),
        api_key=Variable.get("tessera_api_key", default_var=None)
    )
```

Or use an Airflow Connection:

```python
from airflow.hooks.base import BaseHook

def get_tessera_client():
    conn = BaseHook.get_connection("tessera")
    return TesseraClient(
        base_url=f"http://{conn.host}:{conn.port}",
        api_key=conn.password
    )
```

## Sensors

Wait for contract approval:

```python
from airflow.sensors.base import BaseSensorOperator
from tessera_sdk import TesseraClient

class TesseraProposalApprovedSensor(BaseSensorOperator):
    """Wait for a proposal to be approved."""

    def __init__(self, proposal_id: str, tessera_url: str, **kwargs):
        super().__init__(**kwargs)
        self.proposal_id = proposal_id
        self.tessera_url = tessera_url

    def poke(self, context):
        client = TesseraClient(base_url=self.tessera_url)
        proposal = client.proposals.get(self.proposal_id)

        if proposal.status == "approved":
            return True
        elif proposal.status == "rejected":
            raise AirflowException("Proposal was rejected")

        return False
```

## Best Practices

1. **Use environment variables** for Tessera URL and API keys
2. **Add impact checks** before publishing contracts
3. **Handle breaking changes** gracefully with proposal workflows
4. **Retry on transient errors** using Airflow's retry mechanisms
5. **Log contract versions** for audit trails
