import json

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
            assert "AddWorkflow" in data["workflows"]

    def test_execute_and_status_workflow(self):
        with app.test_client() as client:
            payload = {"name": "AddWorkflow", "arguments": [10, 5]}
            response = client.post(
                WORKFLOW_API_URL, headers=HEADERS, data=json.dumps(payload)
            )
            assert response.status_code == 201
            data = response.get_json()
            workflow_id = data.get("workflow_id")
            assert workflow_id

            response = client.get(f"{WORKFLOW_API_URL}/{workflow_id}", headers=HEADERS)
            assert response.status_code == 200
            status_data = response.get_json()
            assert status_data["workflow_id"] == workflow_id
            assert status_data["result"] == 15

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
