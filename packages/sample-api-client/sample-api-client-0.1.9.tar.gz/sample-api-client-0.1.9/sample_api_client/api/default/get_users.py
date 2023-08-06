from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import Response

from typing import cast, List



def _get_kwargs(
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/users".format(
        client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    

    

    

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[str]]:
    if response.status_code == 200:
        response_200 = cast(List[str], response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[str]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,

) -> Response[List[str]]:
    kwargs = _get_kwargs(
        client=client,

    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,

) -> Optional[List[str]]:
    """ Optional extended description in CommonMark or HTML. """

    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,

) -> Response[List[str]]:
    kwargs = _get_kwargs(
        client=client,

    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,

) -> Optional[List[str]]:
    """ Optional extended description in CommonMark or HTML. """

    return (await asyncio_detailed(
        client=client,

    )).parsed
