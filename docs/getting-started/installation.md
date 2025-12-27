# Installation

## Requirements

- Python 3.10+
- httpx >= 0.25.0
- pydantic >= 2.0.0

## Install via pip

```bash
pip install tessera-sdk
```

## Install via uv

```bash
uv add tessera-sdk
```

## Install from source

```bash
git clone https://github.com/ashita-ai/tessera-python.git
cd tessera-python
pip install -e .
```

## Verify installation

```python
from tessera_sdk import TesseraClient

client = TesseraClient(base_url="http://localhost:8000")
print("SDK installed successfully!")
```

## Next steps

- [Quickstart](quickstart.md) - Get up and running
- [Configuration](configuration.md) - Configure authentication
