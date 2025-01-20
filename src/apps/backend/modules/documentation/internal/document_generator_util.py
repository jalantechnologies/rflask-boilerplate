import os
import re
from typing import List

from modules.documentation.errors import ErrorReadingFile
from modules.documentation.types import GetRoutesWithViewDetailsResponse, HttpRouteWithViewDetails
from modules.list_routes.types import HttpRoute


class DocumentGeneratorUtil:
    view_file_suffix = "_view.py"
    router_file_suffix = "_router.py"
    rest_api_folder_path = "rest_api"

    @staticmethod
    def get_routes_with_view_details(params: GetRoutesWithViewDetailsResponse) -> List[HttpRouteWithViewDetails]:
        routes_list: List[HttpRouteWithViewDetails] = []

        for route_with_root_folder_path in params.flask_routes_list:
            rest_api_folder_path = os.path.join(
                route_with_root_folder_path.root_folder_path, DocumentGeneratorUtil.rest_api_folder_path
            )
            for route in route_with_root_folder_path.routes:
                view_method = DocumentGeneratorUtil._get_view_method_code(rest_api_folder_path, route)
                routes_list.append(
                    HttpRouteWithViewDetails(
                        view_method=view_method,
                        endpoint=DocumentGeneratorUtil._get_endpoint(route),
                        method=route.method,
                    )
                )

        return routes_list

    @staticmethod
    def _get_view_method_code(rest_api_folder_path: str, route: HttpRoute) -> str:
        view_method_name = DocumentGeneratorUtil._get_view_method_name(rest_api_folder_path, route)
        if not view_method_name:
            raise ErrorReadingFile(message="Controller method name could not be determined")
        return DocumentGeneratorUtil._extract_method_code_with_signature(
            DocumentGeneratorUtil.view_file_suffix, rest_api_folder_path, f"{view_method_name} ="
        )

    @staticmethod
    def _get_view_method_name(rest_api_folder_path: str, route: HttpRoute) -> str:
        try:
            files = os.listdir(rest_api_folder_path)
            router_file_name = next(
                (file for file in files if file.endswith(DocumentGeneratorUtil.router_file_suffix)), None
            )
            if not router_file_name:
                raise ErrorReadingFile(message="No router file found in rest_api folder: " + rest_api_folder_path)

            router_file_path = os.path.join(rest_api_folder_path, router_file_name)
            with open(router_file_path, "r") as file:
                router_file_content = file.read()

            route_regex = re.compile(
                f"router\\.{route.method.lower()}\\(['\"]{route.router_path}['\"],\\s*ctrl\\.(\\w+)\\)"
            )
            match = route_regex.search(router_file_content)

            if match:
                return match.group(1)

            raise ErrorReadingFile(
                message="No matching route found for method: " + route.method + " and path: " + route.router_path
            )

        except Exception as e:
            raise ErrorReadingFile(message=f"Error reading or writing router file: {str(e)}")

    @staticmethod
    def _get_endpoint(route: HttpRoute) -> str:
        base_api_route_path = DocumentGeneratorUtil._add_leading_slashes_if_not_exists_and_remove_trailing_slashes(
            route.base_api_route_path
        )
        root_router_path = DocumentGeneratorUtil._add_leading_slashes_if_not_exists_and_remove_trailing_slashes(
            route.root_router_path
        )
        router_path = DocumentGeneratorUtil._add_leading_slashes_if_not_exists_and_remove_trailing_slashes(
            route.router_path
        )
        return f"{base_api_route_path}{root_router_path}{router_path}"

    @staticmethod
    def _add_leading_slashes_if_not_exists_and_remove_trailing_slashes(route_path: str) -> str:
        return f"/{route_path.strip('/')}"

    @staticmethod
    def _extract_method_code_with_signature(file_suffix: str, folder_path: str, method_signature: str) -> str:
        try:
            file_name = DocumentGeneratorUtil._find_file_with_suffix(file_suffix, folder_path)
            if not file_name:
                return None

            file_content = DocumentGeneratorUtil._read_file_content(file_name, folder_path)
            method_code = DocumentGeneratorUtil._extract_method_from_content(file_content, method_signature)

            if method_code:
                return method_code.strip()

            raise ErrorReadingFile(message="No matching method found for signature: " + method_signature)

        except Exception as e:
            raise ErrorReadingFile(message=f"Error reading file: {str(e)}")

    @staticmethod
    def _find_file_with_suffix(file_suffix: str, folder_path: str) -> str:
        files = os.listdir(folder_path)
        file_name = next((file for file in files if file.endswith(file_suffix)), None)
        if not file_name:
            raise ErrorReadingFile(message="No file found with suffix: " + file_suffix + " in folder: " + folder_path)
        return file_name

    @staticmethod
    def _read_file_content(file_name: str, folder_path: str) -> str:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r") as file:
            return file.read()

    @staticmethod
    def _extract_method_from_content(file_content: str, method_signature: str) -> str:
        codebase_lines = file_content.split("\n")
        method_code = ""
        is_capturing_codebase = False
        number_of_open_braces = 0

        for line in codebase_lines:
            if not is_capturing_codebase:
                if method_signature in line:
                    is_capturing_codebase = True
                    number_of_open_braces = DocumentGeneratorUtil._count_braces(line)
                    method_code += line + "\n"
                continue

            method_code += line + "\n"
            number_of_open_braces += DocumentGeneratorUtil._count_braces(line)

            if number_of_open_braces == 0:
                break

        return method_code

    @staticmethod
    def _count_braces(line: str) -> int:
        open_braces = len(re.findall(r"[({]", line))
        close_braces = len(re.findall(r"[)}]", line))
        return open_braces - close_braces
