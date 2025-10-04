import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('n8n.env')

# n8n instance details
base_url = os.getenv('N8N_URL', 'https://n8n.getmybot.pro')
api_key = os.getenv('N8N_API_KEY')

def get_workflows():
    """Retrieve all workflows from n8n instance"""
    try:
        # Use API endpoint with API key
        response = requests.get(
            f"{base_url}/api/v1/workflows",
            headers={
                "Accept": "application/json",
                "X-N8N-API-KEY": api_key
            },
            timeout=10
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

def get_workflow_details(workflow_id):
    """Get details of a specific workflow"""
    try:
        response = requests.get(
            f"{base_url}/api/v1/workflows/{workflow_id}",
            headers={
                "Accept": "application/json",
                "X-N8N-API-KEY": api_key
            },
            timeout=10
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting workflow {workflow_id}: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

if __name__ == "__main__":
    print("Connecting to n8n instance...")
    print(f"URL: {base_url}")
    print(f"API Key: {api_key[:20]}..." if api_key else "No API key found!")
    print("-" * 50)

    workflows = get_workflows()

    if workflows:
        if 'data' in workflows:
            workflow_list = workflows['data']
        else:
            workflow_list = workflows

        print(f"\nFound {len(workflow_list)} workflow(s):\n")

        for workflow in workflow_list:
            print(f"ID: {workflow.get('id', 'N/A')}")
            print(f"Name: {workflow.get('name', 'Unnamed')}")
            print(f"Active: {workflow.get('active', False)}")
            print(f"Created: {workflow.get('createdAt', 'N/A')}")
            print(f"Updated: {workflow.get('updatedAt', 'N/A')}")
            print(f"Tags: {', '.join([tag.get('name', '') for tag in workflow.get('tags', [])])}")
            print("-" * 50)

            # Get detailed information for each workflow
            if workflow.get('id'):
                details = get_workflow_details(workflow['id'])
                if details and 'nodes' in details:
                    print(f"Nodes in workflow:")
                    for node in details['nodes']:
                        print(f"  - {node.get('name', 'Unnamed')} ({node.get('type', 'Unknown')})")
                    print("-" * 50)
    else:
        print("Could not retrieve workflows. Please check credentials and API endpoint.")