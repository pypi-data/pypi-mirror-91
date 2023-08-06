# QCS API Client

A client library for accessing the Rigetti QCS API

## Usage

### Synchronous Usage

```python
from qcs_api_client.client import build_sync_client
from qcs_api_client.models import ListReservationsResponseModel
from qcs_api_client.operations.sync import list_reservations

with build_sync_client() as client:
    response: ListReservationsResponse = list_reservations(client=client)
```

### Asynchronous Usage

```python
from qcs_api_client.client import build_async_client
from qcs_api_client.models import ListReservationsResponse
from qcs_api_client.operations.asyncio import list_reservations

async with build_async_client() as client:
    response: ListReservationsResponse = await list_reservations(client=client)
```
