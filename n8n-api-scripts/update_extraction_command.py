"""Update extraction command to use bash/grep only"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('n8n.env')

base_url = os.getenv('N8N_URL')
api_key = os.getenv('N8N_API_KEY')
workflow_id = "UP0MowU4xpBOOE9J"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-N8N-API-KEY": api_key
}

# Get current workflow
response = requests.get(f"{base_url}/api/v1/workflows/{workflow_id}", headers=headers)
workflow = response.json()

# Prepare update
clean_workflow = {
    "name": workflow.get("name"),
    "nodes": workflow.get("nodes"),
    "connections": workflow.get("connections"),
    "settings": workflow.get("settings", {}),
    "staticData": workflow.get("staticData")
}

# Update the Extract website url node with a robust bash command
for node in clean_workflow['nodes']:
    if node['name'] == 'Extract website url':
        # This command:
        # 1. First tries to extract deployment_url from JSON
        # 2. If not found, extracts any buildyoursite.pro URL
        # 3. Handles both output formats
        node['parameters']['command'] = """=echo '{{ $json.stdout }}' | (grep -oP '"deployment_url"\\s*:\\s*"\\K[^"]+' || grep -oP 'https://[a-zA-Z0-9\\-]+\\.buildyoursite\\.pro' | head -1) | head -1"""

        print(f"Updated Extract URL node with robust grep command")

print("\nUpdating workflow...")
update_response = requests.put(
    f"{base_url}/api/v1/workflows/{workflow_id}",
    headers=headers,
    json=clean_workflow
)

if update_response.status_code == 200:
    print("[SUCCESS] Workflow updated!")

    # Activate the workflow
    activate_response = requests.patch(
        f"{base_url}/api/v1/workflows/{workflow_id}",
        headers=headers,
        json={"active": True}
    )

    if activate_response.status_code == 200:
        print("[SUCCESS] Workflow activated!")
    else:
        print(f"[WARNING] Could not activate: {activate_response.text}")
else:
    print(f"[ERROR] Failed: {update_response.text}")