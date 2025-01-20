from dataclasses import dataclass
from typing import List

from modules.list_routes.types import HttpRoute


@dataclass(frozen=True)
class HttpRouteWithRootFolderPath:
    root_folder_path: str
    routes: List[HttpRoute]


@dataclass(frozen=True)
class HttpRouteWithViewDetails:
    view_method: str
    endpoint: str
    method: str


@dataclass(frozen=True)
class MarkdownDocumentation:
    markdown_documentation: str


@dataclass(frozen=True)
class GetRoutesWithViewDetailsResponse:
    flask_routes_list: List[HttpRouteWithRootFolderPath]


class DocumentationErrorCode:
    ERROR_GENERATING_DOCUMENTATION: str = "DOCUMENTATION_ERR_01"
    ERROR_READING_FILE: str = "DOCUMENTATION_ERR_02"
