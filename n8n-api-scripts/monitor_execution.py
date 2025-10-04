"""Monitor workflow execution in real-time"""
import requests
import time
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv('n8n.env')

base_url = os.getenv('N8N_URL')
api_key = os.getenv('N8N_API_KEY')
workflow_id = "UP0MowU4xpBOOE9J"

headers = {
    "Accept": "application/json",
    "X-N8N-API-KEY": api_key
}

print("=" * 60)
print("MONITORING WORKFLOW EXECUTION")
print("=" * 60)
print(f"Workflow: buildyoursite")
print(f"Started monitoring at: {datetime.now().strftime('%H:%M:%S')}")
print("-" * 60)

# Track execution IDs we've seen
seen_executions = set()

# First get recent executions to establish baseline
response = requests.get(
    f"{base_url}/api/v1/executions",
    headers=headers,
    params={"workflowId": workflow_id, "limit": 5}
)

if response.status_code == 200:
    for exec in response.json().get('data', []):
        seen_executions.add(exec['id'])

print(f"Baseline: {len(seen_executions)} recent executions tracked")
print("\nWaiting for new execution to start...")

# Monitor for new executions
check_count = 0
execution_found = False
current_execution_id = None

while check_count < 60:  # Check for up to 5 minutes
    time.sleep(5)  # Check every 5 seconds
    check_count += 1

    response = requests.get(
        f"{base_url}/api/v1/executions",
        headers=headers,
        params={"workflowId": workflow_id, "limit": 10}
    )

    if response.status_code == 200:
        executions = response.json().get('data', [])

        for exec in executions:
            exec_id = exec['id']

            if exec_id not in seen_executions:
                # New execution found!
                seen_executions.add(exec_id)
                current_execution_id = exec_id
                execution_found = True

                print(f"\n[NEW EXECUTION STARTED]")
                print(f"Execution ID: {exec_id}")
                print(f"Started: {exec.get('startedAt', 'N/A')}")

                # Monitor this execution
                while True:
                    detail_response = requests.get(
                        f"{base_url}/api/v1/executions/{exec_id}",
                        headers=headers
                    )

                    if detail_response.status_code == 200:
                        details = detail_response.json()

                        # Check if finished
                        if details.get('finished'):
                            print(f"\n[EXECUTION COMPLETED]")

                            # Calculate duration
                            if details.get('startedAt') and details.get('stoppedAt'):
                                start = datetime.fromisoformat(details['startedAt'].replace('Z', '+00:00'))
                                stop = datetime.fromisoformat(details['stoppedAt'].replace('Z', '+00:00'))
                                duration = (stop - start).total_seconds()
                                print(f"Duration: {duration:.1f} seconds")

                            # Get execution data
                            if 'data' in details and 'resultData' in details['data']:
                                run_data = details['data']['resultData'].get('runData', {})

                                # Check each node's output
                                print("\n[NODE OUTPUTS]")
                                for node_name, node_data in run_data.items():
                                    print(f"\n{node_name}:")

                                    if node_data and len(node_data) > 0:
                                        output = node_data[0].get('json', {})

                                        # Special handling for key nodes
                                        if 'Extract website url' in node_name:
                                            if 'stdout' in output:
                                                url = output['stdout'].strip()
                                                print(f"  [EXTRACTED URL]: {url}")

                                        elif 'Deploy site to with Claude' in node_name:
                                            if 'stdout' in output:
                                                claude_output = output['stdout']
                                                # Look for URL in output
                                                import re
                                                urls = re.findall(r'https://[a-zA-Z0-9\-]+\.buildyoursite\.pro', claude_output)
                                                if urls:
                                                    print(f"  [DEPLOYMENT URL]: {urls[0]}")

                                        elif 'Send email' in node_name:
                                            print(f"  [EMAIL SENT]")

                                        else:
                                            if 'stdout' in output and output['stdout']:
                                                preview = output['stdout'][:100].replace('\n', ' ')
                                                print(f"  Output: {preview}...")

                            # Check for errors
                            if 'data' in details and 'resultData' in details['data']:
                                if 'error' in details['data']['resultData']:
                                    print(f"\n[ERROR]: {details['data']['resultData']['error']}")

                            break  # Exit monitoring loop

                        else:
                            # Still running
                            print(".", end="", flush=True)
                            time.sleep(10)  # Check every 10 seconds

                break  # Exit outer loop after processing execution

    else:
        print(f"Error checking executions: {response.status_code}")

    if not execution_found:
        print(".", end="", flush=True)

if not execution_found:
    print("\n\n[TIMEOUT] No new execution detected within 5 minutes")
    print("The workflow may not have been triggered. Check:")
    print("1. Email was received by info@kiss-it.io")
    print("2. IMAP trigger is configured correctly")
    print("3. Workflow is active")
else:
    print(f"\n\n[MONITORING COMPLETE]")
    if current_execution_id:
        print(f"Execution ID: {current_execution_id}")
        print(f"Check details at: {base_url}/#/executions/{current_execution_id}")