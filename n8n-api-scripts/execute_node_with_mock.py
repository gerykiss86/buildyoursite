"""Execute specific node with mock data via API"""
import requests
import json
import os
import time
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

print("=" * 60)
print("EXECUTE NODE WITH MOCK DATA")
print("=" * 60)

# Mock Claude output - typical format from your examples
mock_claude_output = {
    "error": None,
    "job_id": "test-mock-execution",
    "output": "https://alpine-digital.buildyoursite.pro\n\n```json\n{\n  \"report\": {\n    \"site_name\": \"Alpine Digital\",\n    \"company_name\": \"Alpine Digital Services\",\n    \"deployment_url\": \"https://alpine-digital.buildyoursite.pro\",\n    \"image_generation_prompts\": [\n      \"modern digital agency office\",\n      \"web development workspace\",\n      \"creative design studio\"\n    ]\n  }\n}\n```\n",
    "return_code": 0,
    "status": "completed"
}

print("\nMock Claude output prepared:")
print("Expected URL: https://alpine-digital.buildyoursite.pro")

# Execute workflow with pinned data
print("\n" + "-" * 60)
print("Executing workflow with mock data...")

# Create execution request
execution_payload = {
    "workflowData": {
        "id": workflow_id,
        "name": "buildyoursite-test"
    },
    "pinData": {
        "Deploy site to with Claude": [
            {
                "json": {
                    "stdout": json.dumps(mock_claude_output),
                    "stderr": "",
                    "returnCode": 0
                }
            }
        ]
    }
}

# Try to execute
response = requests.post(
    f"{base_url}/api/v1/workflows/{workflow_id}/execute",
    headers=headers,
    json=execution_payload
)

if response.status_code == 200:
    result = response.json()
    print("[SUCCESS] Workflow execution started")
    print(f"Execution ID: {result.get('id', 'N/A')}")

    # Wait a bit for execution to complete
    print("\nWaiting for execution to complete...")
    time.sleep(5)

    # Check execution result
    if result.get('id'):
        exec_response = requests.get(
            f"{base_url}/api/v1/executions/{result['id']}",
            headers=headers
        )

        if exec_response.status_code == 200:
            exec_details = exec_response.json()

            if 'data' in exec_details and 'resultData' in exec_details['data']:
                run_data = exec_details['data']['resultData'].get('runData', {})

                # Check Extract URL node result
                for node_name, node_data in run_data.items():
                    if 'Extract website url' in node_name:
                        if node_data and len(node_data) > 0:
                            output = node_data[0].get('json', {})
                            if 'stdout' in output:
                                extracted_url = output['stdout'].strip()
                                print(f"\n[RESULT] Extracted URL: {extracted_url}")

                                if extracted_url == "https://alpine-digital.buildyoursite.pro":
                                    print("[SUCCESS] URL extracted correctly!")
                                else:
                                    print("[WARNING] URL doesn't match expected")
else:
    print(f"[ERROR] Failed to execute: {response.status_code}")
    print(response.text)
    print("\nTrying alternative approach...")

print("\n" + "=" * 60)
print("ALTERNATIVE: Direct API Test")
print("=" * 60)

# Test the extraction logic directly
print("\nTesting extraction patterns on mock data:")

test_outputs = [
    {
        "name": "Format 1 - Direct URL + JSON",
        "json_output": json.dumps(mock_claude_output)
    },
    {
        "name": "Format 2 - Embedded in output field",
        "json_output": json.dumps({
            "error": None,
            "output": "https://test-site.buildyoursite.pro\n\n{\"report\":{\"deployment_url\":\"https://test-site.buildyoursite.pro\"}}",
            "status": "completed"
        })
    }
]

import re

for test in test_outputs:
    print(f"\nTest: {test['name']}")
    data = test['json_output']

    # Try parsing as JSON
    try:
        parsed = json.loads(data)
        if 'output' in parsed and parsed['output']:
            output_text = parsed['output']

            # Method 1: Look for deployment_url in JSON
            url_match = re.search(r'"deployment_url"\s*:\s*"([^"]+)"', output_text)
            if url_match:
                print(f"  Found via deployment_url: {url_match.group(1)}")
                continue

            # Method 2: Direct URL pattern
            url_match = re.search(r'https://[a-zA-Z0-9\-]+\.buildyoursite\.pro', output_text)
            if url_match:
                print(f"  Found via URL pattern: {url_match.group(0)}")
            else:
                print("  No URL found")
    except json.JSONDecodeError:
        print("  Failed to parse JSON")

print("\n" + "=" * 60)
print("MANUAL TESTING INSTRUCTIONS")
print("=" * 60)
print("\nTo test manually in n8n UI:")
print("1. Open workflow: https://n8n.y2k.global/#/workflow/" + workflow_id)
print("2. Click on 'Deploy site to with Claude' node")
print("3. In the output panel, click the pin icon")
print("4. Replace the output with this mock data:")
print("-" * 40)
print(json.dumps({
    "stdout": json.dumps(mock_claude_output),
    "stderr": "",
    "returnCode": 0
}, indent=2))
print("-" * 40)
print("5. Save the pinned data")
print("6. Click on 'Extract website url' node")
print("7. Click 'Execute Node' to test just this node")
print("8. Check the output - it should show: https://alpine-digital.buildyoursite.pro")