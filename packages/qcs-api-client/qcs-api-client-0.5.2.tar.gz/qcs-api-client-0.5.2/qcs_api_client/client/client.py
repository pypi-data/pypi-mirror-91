from contextlib import asynccontextmanager, contextmanager
from typing import Optional

import httpx

from qcs_api_client.client._configuration import QCSClientConfiguration
from qcs_api_client.client.auth import QCSAuth, QCSAuthConfiguration


def _build_client_kwargs(*, configuration: Optional[QCSClientConfiguration] = None) -> dict:
    """
    Return kwargs used for construction of an httpx.BaseClient.
    """
    configuration = configuration or QCSClientConfiguration.load()
    auth_configuration = QCSAuthConfiguration(
        auth_server=configuration.auth_server,
    )
    auth = QCSAuth(
        client_configuration=configuration,
        auth_configuration=auth_configuration,
    )
    return dict(auth=auth, base_url=configuration.profile.api_url)


@contextmanager
def build_sync_client(*, configuration: Optional[QCSClientConfiguration] = None) -> httpx.Client:
    """
    Yield a client object suitable for use with the qcs_api_client.sync API functions.
    """
    with httpx.Client(**_build_client_kwargs(configuration=configuration)) as client:
        yield client


@asynccontextmanager
async def build_async_client(*, configuration: Optional[QCSClientConfiguration] = None) -> httpx.AsyncClient:
    """
    Yield a client object suitable for use with the qcs_api_client.asyncio API functions.
    """
    async with httpx.AsyncClient(**_build_client_kwargs(configuration=configuration)) as client:
        yield client
