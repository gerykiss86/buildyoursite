"""Update workflow with cleaned data"""
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
if response.status_code != 200:
    print(f"Error fetching workflow: {response.status_code}")
    exit(1)

workflow = response.json()

# Keep only the fields n8n API expects (without read-only fields)
clean_workflow = {
    "name": workflow.get("name"),
    "nodes": workflow.get("nodes"),
    "connections": workflow.get("connections"),
    "settings": workflow.get("settings", {}),
    "staticData": workflow.get("staticData")
}

# Update the Extract website url node with a better extraction command
for node in clean_workflow['nodes']:
    if node['name'] == 'Extract website url':
        # Use a simpler bash command that handles both formats
        node['parameters']['command'] = """=echo '{{ $json.stdout }}' | python3 -c "
import sys, json, re
data = sys.stdin.read()

# Try to parse as JSON first
try:
    parsed = json.loads(data)
    if 'output' in parsed:
        output = parsed['output']
        # Look for deployment_url in report
        match = re.search(r'\"deployment_url\"\\s*:\\s*\"([^\"]+)\"', output)
        if match:
            print(match.group(1))
            sys.exit(0)
        # Look for any buildyoursite URL
        match = re.search(r'https://[a-zA-Z0-9\\-]+\\.buildyoursite\\.pro', output)
        if match:
            print(match.group(0))
            sys.exit(0)
except:
    pass

# Direct pattern matching on raw output
# Look for deployment_url
match = re.search(r'\"deployment_url\"\\s*:\\s*\"([^\"]+)\"', data)
if match:
    print(match.group(1))
    sys.exit(0)

# Look for any buildyoursite URL
match = re.search(r'https://[a-zA-Z0-9\\-]+\\.buildyoursite\\.pro', data)
if match:
    print(match.group(0))
else:
    print('URL_NOT_FOUND')
"
"""
        print(f"Updated Extract URL node")

# Save the updated workflow
update_response = requests.put(
    f"{base_url}/api/v1/workflows/{workflow_id}",
    headers=headers,
    json=clean_workflow
)

if update_response.status_code == 200:
    print("[SUCCESS] Workflow updated!")
else:
    print(f"[ERROR] Failed to update: {update_response.status_code}")
    print(update_response.text)