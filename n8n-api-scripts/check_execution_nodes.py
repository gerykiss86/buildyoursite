"""Check what nodes are present in executions"""
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

exec_id = 287  # Recent execution

print(f"Checking execution {exec_id}...")

response = requests.get(
    f"{base_url}/api/v1/executions/{exec_id}",
    headers=headers
)

if response.status_code == 200:
    details = response.json()

    # Save full response
    with open(f'execution_{exec_id}_full.json', 'w') as f:
        json.dump(details, f, indent=2)

    print(f"Full execution saved to: execution_{exec_id}_full.json")

    # Check structure
    print("\nExecution structure:")
    print(f"- finished: {details.get('finished')}")
    print(f"- status: {details.get('status')}")
    print(f"- mode: {details.get('mode')}")

    # Check if there's data
    if 'data' in details:
        print("\nHas 'data' field")

        if 'resultData' in details['data']:
            print("Has 'resultData' field")

            result_data = details['data']['resultData']

            if 'runData' in result_data:
                run_data = result_data['runData']
                print(f"\nFound {len(run_data)} nodes with data:")

                for node_name in run_data.keys():
                    print(f"  - {node_name}")

                    # Check Deploy site node specifically
                    if "Deploy" in node_name and "Claude" in node_name:
                        node_data = run_data[node_name]
                        print(f"\n[CLAUDE NODE DATA]:")
                        if node_data and len(node_data) > 0:
                            output = node_data[0].get('json', {})
                            if 'stdout' in output:
                                stdout = output['stdout']
                                print(f"stdout length: {len(stdout)} chars")
                                print(f"First 200 chars: {stdout[:200]}")

                                # Save to file
                                with open(f'claude_output_{exec_id}.txt', 'w', encoding='utf-8') as f:
                                    f.write(stdout)
                                print(f"Saved to: claude_output_{exec_id}.txt")
                            else:
                                print("No stdout in output")
                        else:
                            print("No data in node")

                    # Check Extract node
                    if "Extract" in node_name and "url" in node_name.lower():
                        node_data = run_data[node_name]
                        print(f"\n[EXTRACT NODE DATA]:")
                        if node_data and len(node_data) > 0:
                            output = node_data[0].get('json', {})
                            print(f"Output: {output}")

            else:
                print("No 'runData' in resultData")

            # Check for error
            if 'error' in result_data:
                print(f"\nError in execution: {result_data['error']}")

            # Check for lastNodeExecuted
            if 'lastNodeExecuted' in result_data:
                print(f"\nLast node executed: {result_data['lastNodeExecuted']}")

else:
    print(f"Error: {response.status_code}")
    print(response.text)