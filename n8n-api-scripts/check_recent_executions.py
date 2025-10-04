"""Check recent workflow executions"""
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('n8n.env')

base_url = os.getenv('N8N_URL')
api_key = os.getenv('N8N_API_KEY')
workflow_id = "UP0MowU4xpBOOE9J"

headers = {
    "Accept": "application/json",
    "X-N8N-API-KEY": api_key
}

print("Checking recent executions...")

response = requests.get(
    f"{base_url}/api/v1/executions",
    headers=headers,
    params={"workflowId": workflow_id, "limit": 10}
)

if response.status_code == 200:
    executions = response.json().get('data', [])

    print(f"\nFound {len(executions)} recent executions:\n")

    for exec in executions[:5]:
        exec_id = exec['id']
        started = exec.get('startedAt', 'N/A')
        finished = exec.get('finished', False)
        status = "Completed" if finished else "Running/Failed"

        print(f"ID: {exec_id}")
        print(f"  Started: {started}")
        print(f"  Status: {status}")

        if exec.get('stoppedAt'):
            start = datetime.fromisoformat(exec['startedAt'].replace('Z', '+00:00'))
            stop = datetime.fromisoformat(exec['stoppedAt'].replace('Z', '+00:00'))
            duration = (stop - start).total_seconds()
            print(f"  Duration: {duration:.0f} seconds")

        print("-" * 40)

else:
    print(f"Error: {response.status_code}")