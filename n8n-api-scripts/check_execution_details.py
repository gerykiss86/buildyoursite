"""Check details of recent execution"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('n8n.env')

base_url = os.getenv('N8N_URL')
api_key = os.getenv('N8N_API_KEY')

headers = {
    "Accept": "application/json",
    "X-N8N-API-KEY": api_key
}

# Check the most recent execution
exec_id = 290

print(f"Checking execution {exec_id} details...")

response = requests.get(
    f"{base_url}/api/v1/executions/{exec_id}",
    headers=headers
)

if response.status_code == 200:
    details = response.json()

    print(f"\nExecution ID: {exec_id}")
    print(f"Status: {'Finished' if details.get('finished') else 'Not finished'}")
    print(f"Mode: {details.get('mode', 'N/A')}")

    if 'data' in details and 'resultData' in details['data']:
        result_data = details['data']['resultData']

        # Check for errors
        if 'error' in result_data:
            print(f"\n[ERROR]: {result_data['error']}")

        # Check last node executed
        if 'lastNodeExecuted' in result_data:
            print(f"\nLast node executed: {result_data['lastNodeExecuted']}")

        # Get execution data
        run_data = result_data.get('runData', {})

        if run_data:
            print(f"\nNodes executed: {len(run_data)}")
            for node_name in run_data.keys():
                print(f"  - {node_name}")

                # Check for errors in nodes
                node_data = run_data[node_name]
                if node_data and len(node_data) > 0:
                    if 'error' in node_data[0]:
                        print(f"    ERROR: {node_data[0]['error']}")
        else:
            print("\nNo nodes were executed")

        # Check trigger data
        if 'Email Trigger (IMAP)' in run_data:
            trigger_data = run_data['Email Trigger (IMAP)']
            if trigger_data and len(trigger_data) > 0:
                output = trigger_data[0].get('json', {})
                print(f"\nEmail trigger output:")
                print(f"  Subject: {output.get('subject', 'N/A')}")
                print(f"  From: {output.get('from', 'N/A')}")
                print(f"  Text preview: {output.get('textContent', '')[:100]}")

else:
    print(f"Error: {response.status_code}")

# Also check if IMAP trigger is working
print("\n" + "=" * 60)
print("CHECKING IMAP TRIGGER CONFIGURATION")
print("=" * 60)

# Get workflow to check trigger settings
workflow_response = requests.get(
    f"{base_url}/api/v1/workflows/UP0MowU4xpBOOE9J",
    headers=headers
)

if workflow_response.status_code == 200:
    workflow = workflow_response.json()

    for node in workflow['nodes']:
        if node['name'] == 'Email Trigger (IMAP)':
            print("\nIMAP Trigger found:")
            params = node.get('parameters', {})
            print(f"  Post-process action: {params.get('postProcessAction', 'N/A')}")

            # Check if node has credentials
            if 'credentials' in node:
                print(f"  Has credentials: Yes")
                cred_info = node['credentials'].get('imap', {})
                print(f"  Credential ID: {cred_info.get('id', 'N/A')}")
                print(f"  Credential name: {cred_info.get('name', 'N/A')}")