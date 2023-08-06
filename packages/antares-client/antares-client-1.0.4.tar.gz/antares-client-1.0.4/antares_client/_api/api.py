from typing import Any, Dict, List, Iterator, Optional, Type

import requests
from marshmallow_jsonapi import Schema
from typing_extensions import TypedDict

from antares_client.exceptions import AntaresException

PageParam = TypedDict(
    "PageParam",
    {
        "limit": int,
        "offset": int,
    },
)

QueryParams = TypedDict(
    "QueryParams",
    {
        "sort": str,
        "page": PageParam,
        "fields": Dict[str, List[str]],
        "elasticsearch_query": Dict,
        # "filter": None  # RESERVED
    },
)


def _get_resource(
    url: str, schema_cls: Type[Schema], params: Optional[QueryParams] = None
) -> Optional[Any]:
    response = requests.get(url, params=params)
    if response.status_code == 404:
        return None
    if response.status_code >= 400:
        raise AntaresException(response.json())
    return schema_cls(partial=True).load(response.json())


def _list_resources(
    url: str, schema_cls: Type[Schema], params: Optional[QueryParams] = None
) -> Iterator[Any]:
    response = requests.get(url, params=params)
    if response.status_code >= 400:
        raise AntaresException(response.json())
    yield from schema_cls(many=True, partial=True).load(response.json())


def _list_all_resources(
    url: str, schema_cls: Type[Schema], params: Optional[QueryParams] = None
) -> Iterator[Any]:
    while True:
        response = requests.get(url, params=params)
        if response.status_code >= 400:
            raise AntaresException(response.json())
        yield from schema_cls(many=True, partial=True).load(response.json())
        url = response.json().get("links", {}).get("next")
        if url is None:
            break
        params = None
