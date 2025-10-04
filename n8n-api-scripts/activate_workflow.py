"""Activate the workflow"""
import requests
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

print(f"Current workflow status: {'Active' if workflow.get('active') else 'Inactive'}")

if not workflow.get('active'):
    # Activate by updating with active=true
    workflow['active'] = True

    # Keep only updatable fields
    update_data = {
        "name": workflow.get("name"),
        "nodes": workflow.get("nodes"),
        "connections": workflow.get("connections"),
        "settings": workflow.get("settings", {}),
        "staticData": workflow.get("staticData"),
        "active": True
    }

    update_response = requests.put(
        f"{base_url}/api/v1/workflows/{workflow_id}",
        headers=headers,
        json=update_data
    )

    if update_response.status_code == 200:
        print("[SUCCESS] Workflow activated!")
    else:
        print(f"[ERROR] Failed to activate: {update_response.text}")
else:
    print("Workflow is already active")