from typing import TypedDict


class HttpRoute(TypedDict):
    base_api_route_path: str
    method: str
    root_router_path: str
    router_path: str
