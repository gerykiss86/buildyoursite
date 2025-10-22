"""
n8n Workflow Manager - Complete API interaction script
"""

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import time

# Load environment variables
load_dotenv('n8n.env')

class N8NWorkflowManager:
    def __init__(self):
        self.base_url = os.getenv('N8N_URL', 'https://n8n.y2k.global')
        self.api_key = os.getenv('N8N_API_KEY')
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-N8N-API-KEY": self.api_key
        }

    def get_all_workflows(self):
        """Get all workflows"""
        response = requests.get(f"{self.base_url}/api/v1/workflows", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_workflow(self, workflow_id):
        """Get specific workflow details"""
        response = requests.get(f"{self.base_url}/api/v1/workflows/{workflow_id}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def activate_workflow(self, workflow_id):
        """Activate a workflow"""
        response = requests.patch(
            f"{self.base_url}/api/v1/workflows/{workflow_id}",
            headers=self.headers,
            json={"active": True}
        )
        return response.status_code == 200

    def deactivate_workflow(self, workflow_id):
        """Deactivate a workflow"""
        response = requests.patch(
            f"{self.base_url}/api/v1/workflows/{workflow_id}",
            headers=self.headers,
            json={"active": False}
        )
        return response.status_code == 200

    def execute_workflow(self, workflow_id, data=None):
        """Execute a workflow manually"""
        payload = {"workflowData": data} if data else {}
        response = requests.post(
            f"{self.base_url}/api/v1/workflows/{workflow_id}/execute",
            headers=self.headers,
            json=payload
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error executing workflow: {response.status_code} - {response.text}")
            return None

    def get_executions(self, workflow_id=None, limit=10):
        """Get workflow executions"""
        url = f"{self.base_url}/api/v1/executions"
        params = {"limit": limit}
        if workflow_id:
            params["workflowId"] = workflow_id

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_execution(self, execution_id):
        """Get specific execution details"""
        response = requests.get(f"{self.base_url}/api/v1/executions/{execution_id}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def delete_execution(self, execution_id):
        """Delete an execution"""
        response = requests.delete(f"{self.base_url}/api/v1/executions/{execution_id}", headers=self.headers)
        return response.status_code == 200

    def get_credentials(self):
        """Get all credentials (without sensitive data)"""
        response = requests.get(f"{self.base_url}/api/v1/credentials", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def test_webhook(self, webhook_url, data):
        """Test a webhook endpoint"""
        response = requests.post(webhook_url, json=data, timeout=30)
        return {
            "status_code": response.status_code,
            "response": response.text,
            "headers": dict(response.headers)
        }

def main():
    """Main function to demonstrate usage"""
    manager = N8NWorkflowManager()

    print("=" * 60)
    print("N8N WORKFLOW MANAGER")
    print("=" * 60)

    while True:
        print("\nOptions:")
        print("1. List all workflows")
        print("2. Get workflow details")
        print("3. Activate workflow")
        print("4. Deactivate workflow")
        print("5. Execute workflow")
        print("6. List recent executions")
        print("7. Get execution details")
        print("8. Delete execution")
        print("9. List credentials")
        print("0. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            workflows = manager.get_all_workflows()
            if workflows and 'data' in workflows:
                for wf in workflows['data']:
                    status = "✅ Active" if wf.get('active') else "❌ Inactive"
                    print(f"\n{status} ID: {wf['id']}")
                    print(f"   Name: {wf['name']}")
                    print(f"   Created: {wf.get('createdAt', 'N/A')}")
                    print(f"   Updated: {wf.get('updatedAt', 'N/A')}")

        elif choice == "2":
            workflow_id = input("Enter workflow ID: ")
            workflow = manager.get_workflow(workflow_id)
            if workflow:
                print(f"\nWorkflow: {workflow.get('name')}")
                print(f"Active: {workflow.get('active')}")
                print(f"Nodes: {len(workflow.get('nodes', []))}")
                for node in workflow.get('nodes', []):
                    print(f"  - {node['name']} ({node['type']})")

        elif choice == "3":
            workflow_id = input("Enter workflow ID to activate: ")
            if manager.activate_workflow(workflow_id):
                print("✅ Workflow activated successfully")
            else:
                print("❌ Failed to activate workflow")

        elif choice == "4":
            workflow_id = input("Enter workflow ID to deactivate: ")
            if manager.deactivate_workflow(workflow_id):
                print("✅ Workflow deactivated successfully")
            else:
                print("❌ Failed to deactivate workflow")

        elif choice == "5":
            workflow_id = input("Enter workflow ID to execute: ")
            data_input = input("Enter JSON data (or press Enter for none): ")
            data = json.loads(data_input) if data_input else None
            result = manager.execute_workflow(workflow_id, data)
            if result:
                print(f"✅ Workflow executed: {result.get('id')}")

        elif choice == "6":
            workflow_id = input("Enter workflow ID (or press Enter for all): ")
            workflow_id = workflow_id if workflow_id else None
            executions = manager.get_executions(workflow_id)
            if executions and 'data' in executions:
                for exc in executions['data']:
                    status = "✅" if exc.get('finished') else "⏳"
                    print(f"\n{status} ID: {exc['id']}")
                    print(f"   Workflow: {exc.get('workflowId')}")
                    print(f"   Started: {exc.get('startedAt')}")
                    print(f"   Status: {exc.get('status')}")

        elif choice == "7":
            execution_id = input("Enter execution ID: ")
            execution = manager.get_execution(execution_id)
            if execution:
                print(f"\nExecution ID: {execution['id']}")
                print(f"Status: {execution.get('status')}")
                print(f"Started: {execution.get('startedAt')}")
                print(f"Finished: {execution.get('stoppedAt')}")
                if 'data' in execution and 'resultData' in execution['data']:
                    print(f"Output nodes: {len(execution['data']['resultData'].get('runData', {}))}")

        elif choice == "8":
            execution_id = input("Enter execution ID to delete: ")
            if manager.delete_execution(execution_id):
                print("✅ Execution deleted successfully")
            else:
                print("❌ Failed to delete execution")

        elif choice == "9":
            credentials = manager.get_credentials()
            if credentials and 'data' in credentials:
                for cred in credentials['data']:
                    print(f"\nID: {cred['id']}")
                    print(f"   Name: {cred['name']}")
                    print(f"   Type: {cred['type']}")

        elif choice == "0":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()