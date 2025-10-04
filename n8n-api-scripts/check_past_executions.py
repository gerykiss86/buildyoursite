"""Check past workflow executions to analyze Claude output formats"""
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('n8n.env')

base_url = os.getenv('N8N_URL')
api_key = os.getenv('N8N_API_KEY')
workflow_id = "UP0MowU4xpBOOE9J"  # buildyoursite workflow

headers = {
    "Accept": "application/json",
    "X-N8N-API-KEY": api_key
}

# Get recent executions
print("Fetching recent workflow executions...")
response = requests.get(
    f"{base_url}/api/v1/executions",
    headers=headers,
    params={"workflowId": workflow_id, "limit": 50}
)

if response.status_code == 200:
    executions = response.json()

    print(f"Found {len(executions.get('data', []))} executions\n")

    # Filter for successful executions that ran longer than 5 minutes
    long_running = []

    for exec in executions.get('data', []):
        if exec.get('stoppedAt') and exec.get('startedAt'):
            start = datetime.fromisoformat(exec['startedAt'].replace('Z', '+00:00'))
            stop = datetime.fromisoformat(exec['stoppedAt'].replace('Z', '+00:00'))
            duration = (stop - start).total_seconds()

            if duration > 300:  # More than 5 minutes
                long_running.append({
                    'id': exec['id'],
                    'duration': duration,
                    'status': exec.get('status'),
                    'finished': exec.get('finished'),
                    'startedAt': exec.get('startedAt')
                })

    print(f"Found {len(long_running)} executions that ran longer than 5 minutes:\n")

    # Get details for each long-running execution
    for exec_summary in long_running[:5]:  # Check last 5 long-running executions
        exec_id = exec_summary['id']
        print(f"\n{'='*60}")
        print(f"Execution ID: {exec_id}")
        print(f"Duration: {exec_summary['duration']:.0f} seconds")
        print(f"Status: {exec_summary['status']}")
        print(f"Started: {exec_summary['startedAt']}")

        # Get full execution details
        detail_response = requests.get(
            f"{base_url}/api/v1/executions/{exec_id}",
            headers=headers
        )

        if detail_response.status_code == 200:
            details = detail_response.json()

            # Look for Claude deployment node output
            if 'data' in details and 'resultData' in details['data']:
                run_data = details['data']['resultData'].get('runData', {})

                # Find Claude deployment node
                for node_name, node_data in run_data.items():
                    if 'Claude' in node_name or 'claude' in node_name.lower():
                        print(f"\nFound Claude node: {node_name}")

                        if node_data and len(node_data) > 0:
                            output = node_data[0].get('json', {})

                            # Check stdout
                            if 'stdout' in output:
                                stdout = output['stdout']
                                print(f"\nClaude stdout output (first 500 chars):")
                                print("-" * 40)
                                print(stdout[:500])

                                # Try to find URLs in different formats
                                print("\nSearching for URLs...")

                                # Check for direct URL
                                if 'https://' in stdout:
                                    import re
                                    urls = re.findall(r'https://[^\s"\'<>]+', stdout)
                                    if urls:
                                        print(f"Found URLs: {urls}")

                                # Check for JSON with output field
                                if '"output"' in stdout:
                                    print("Found 'output' field in response")
                                    try:
                                        # Extract JSON portion
                                        json_start = stdout.find('{')
                                        json_end = stdout.rfind('}') + 1
                                        if json_start >= 0 and json_end > json_start:
                                            json_str = stdout[json_start:json_end]
                                            parsed = json.loads(json_str)
                                            if 'output' in parsed:
                                                print(f"Output field: {parsed['output'][:200]}")
                                    except:
                                        pass

                                # Check for deploymentUrl field
                                if 'deploymentUrl' in stdout or 'deployment_url' in stdout:
                                    print("Found 'deploymentUrl' field in response")
                                    try:
                                        json_start = stdout.find('{')
                                        json_end = stdout.rfind('}') + 1
                                        if json_start >= 0 and json_end > json_start:
                                            json_str = stdout[json_start:json_end]
                                            parsed = json.loads(json_str)
                                            if 'deploymentUrl' in parsed:
                                                print(f"deploymentUrl: {parsed['deploymentUrl']}")
                                            if 'deployment_url' in parsed:
                                                print(f"deployment_url: {parsed['deployment_url']}")
                                    except:
                                        pass

                                # Save full output for analysis
                                filename = f"execution_{exec_id}_claude_output.txt"
                                with open(filename, 'w', encoding='utf-8') as f:
                                    f.write(stdout)
                                print(f"\nFull output saved to: {filename}")

                # Also check Extract URL node
                for node_name, node_data in run_data.items():
                    if 'Extract' in node_name and 'url' in node_name.lower():
                        print(f"\nFound Extract URL node: {node_name}")

                        if node_data and len(node_data) > 0:
                            output = node_data[0].get('json', {})
                            if 'stdout' in output:
                                print(f"Extracted URL: {output['stdout'][:200]}")

else:
    print(f"Error fetching executions: {response.status_code}")
    print(response.text)