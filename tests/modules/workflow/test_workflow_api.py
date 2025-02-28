import json
import time

from tests.modules.workflow.base_test_workflow import BaseTestWorkflow

from modules.workflow.types import WorkflowErrorCode
from server import app

WORKFLOW_API_URL = "http://127.0.0.1:8080/api/workflows"
HEADERS = {"Content-Type": "application/json"}


class TestWorkflowApi(BaseTestWorkflow):
    def test_get_workflow_list(self):
        with app.test_client() as client:
            response = client.get(WORKFLOW_API_URL, headers=HEADERS)
            data = response.get_json()
            assert response.status_code == 200
            assert "workflows" in data
            assert {"name": "TestDefaultWorkflow", "priority": "default"} in data[
                "workflows"
            ]

    def test_queue_and_get_details_workflow(self):
        with app.test_client() as client:
            payload = {"name": "TestDefaultWorkflow", "arguments": [10, 5]}
            response = client.post(
                WORKFLOW_API_URL, headers=HEADERS, data=json.dumps(payload)
            )
            assert response.status_code == 201
            data = response.get_json()
            workflow_id = data.get("workflow_id")
            assert workflow_id

            time.sleep(1)

            response = client.get(f"{WORKFLOW_API_URL}/{workflow_id}", headers=HEADERS)
            assert response.status_code == 200
            data = response.get_json()
            assert data["workflow_id"] == workflow_id
            assert int(data["runs"][0]["result"]) == 15

    def test_execute_workflow_invalid_workflow_name(self):
        with app.test_client() as client:
            payload = {"name": "non_existent", "arguments": [10, 5]}
            response = client.post(
                WORKFLOW_API_URL, headers=HEADERS, data=json.dumps(payload)
            )
            assert response.status_code == 404
            data = response.get_json()
            assert data["code"] == WorkflowErrorCode.WORKFLOW_WITH_NAME_NOT_FOUND

    def test_get_workflow_status_invalid_workflow_id(self):
        with app.test_client() as client:
            response = client.get(f"{WORKFLOW_API_URL}/invalid_id", headers=HEADERS)
            assert response.status_code == 404
            data = response.get_json()
            assert data["code"] == WorkflowErrorCode.WORKFLOW_WITH_ID_NOT_FOUND
