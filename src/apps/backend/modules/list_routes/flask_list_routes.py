from modules.list_routes.types import HttpRoute
from flask import Flask
from typing import List

class FlaskListRoutes:
    @staticmethod
    def list_routes(app: Flask, base_api_route_path: str) -> List[HttpRoute]:
        routes = []
        for rule in app.url_map.iter_rules():
            method = rule.methods
            for m in method:
                # Extract rootRouterPath and routerPath correctly
                # Skip OPTIONS and HEAD method
                if m == 'OPTIONS' or m=='HEAD':
                    continue
                full_path = rule.rule
                root_router_path = '/' + full_path.split('/')[2]
                router_path = '/' + full_path.split('/')[3] if len(full_path.split('/')) > 3 else '/'

                routes.append({
                    "base_api_route_path": base_api_route_path,
                    "method": m,
                    "root_router_path": root_router_path,
                    "router_path": router_path
                })
        return routes
