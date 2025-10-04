"""Get detailed workflow configuration"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('n8n.env')

base_url = os.getenv('N8N_URL')
api_key = os.getenv('N8N_API_KEY')
workflow_id = "UP0MowU4xpBOOE9J"  # buildyoursite workflow

headers = {
    "Accept": "application/json",
    "X-N8N-API-KEY": api_key
}

# Get workflow details
response = requests.get(f"{base_url}/api/v1/workflows/{workflow_id}", headers=headers)

if response.status_code == 200:
    workflow = response.json()

    # Save full workflow to file for analysis
    with open('workflow_full.json', 'w') as f:
        json.dump(workflow, f, indent=2)

    print("Workflow Details:")
    print(f"Name: {workflow.get('name')}")
    print(f"Active: {workflow.get('active')}")
    print(f"\nNodes ({len(workflow.get('nodes', []))}):")

    # Find and display Claude and Extract nodes
    claude_node = None
    extract_node = None

    for node in workflow.get('nodes', []):
        print(f"\n- {node['name']} ({node['type']})")

        if "Claude" in node['name'] or "claude" in node['name'].lower():
            claude_node = node
            print(f"  [CLAUDE NODE FOUND]")

        if "Extract" in node['name'] and "url" in node['name'].lower():
            extract_node = node
            print(f"  [EXTRACT NODE FOUND]")

    # Display Claude node details
    if claude_node:
        print("\n" + "="*60)
        print("CLAUDE DEPLOYMENT NODE CONFIGURATION:")
        print("="*60)
        print(f"Name: {claude_node['name']}")
        print(f"Type: {claude_node['type']}")

        if 'parameters' in claude_node:
            print("\nParameters:")
            print(json.dumps(claude_node['parameters'], indent=2))

    # Display Extract node details
    if extract_node:
        print("\n" + "="*60)
        print("URL EXTRACTION NODE CONFIGURATION:")
        print("="*60)
        print(f"Name: {extract_node['name']}")
        print(f"Type: {extract_node['type']}")

        if 'parameters' in extract_node:
            print("\nParameters:")
            print(json.dumps(extract_node['parameters'], indent=2))

    print("\nFull workflow saved to: workflow_full.json")

else:
    print(f"Error: {response.status_code}")
    print(response.text)