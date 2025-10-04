"""Test specific nodes with mock data"""
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

print("=" * 60)
print("TESTING NODES WITH MOCK DATA")
print("=" * 60)

# First, get the workflow
response = requests.get(f"{base_url}/api/v1/workflows/{workflow_id}", headers=headers)
if response.status_code != 200:
    print(f"Error fetching workflow: {response.status_code}")
    exit(1)

workflow = response.json()

# Find the nodes we need
parse_node = None
bolt_node = None
claude_node = None
extract_node = None

for node in workflow['nodes']:
    if node['name'] == 'Parse output folder':
        parse_node = node
    elif node['name'] == 'Generate Site with Bolt':
        bolt_node = node
    elif node['name'] == 'Deploy site to with Claude':
        claude_node = node
    elif node['name'] == 'Extract website url':
        extract_node = node

print("\nFound nodes:")
if parse_node:
    print(f"✓ Parse output folder: {parse_node['id']}")
if bolt_node:
    print(f"✓ Generate Site with Bolt: {bolt_node['id']}")
if claude_node:
    print(f"✓ Deploy site to with Claude: {claude_node['id']}")
if extract_node:
    print(f"✓ Extract website url: {extract_node['id']}")

# Create a test workflow with just the nodes we want to test
print("\n" + "-" * 60)
print("Creating test workflow...")

# Mock data for the Bolt output (what Parse output folder would produce)
mock_bolt_output = "/bolt-output/generated-site-2024-01-04-test.zip"

# Mock data that would come from Claude deployment
mock_claude_output = {
    "error": None,
    "job_id": "test-123-456",
    "output": "https://test-company.buildyoursite.pro\\n\\n```json\\n{\\n  \"report\": {\\n    \"site_name\": \"Test Company\",\\n    \"company_name\": \"Test Company GmbH\",\\n    \"deployment_url\": \"https://test-company.buildyoursite.pro\",\\n    \"image_generation_prompts\": [\\n      \"modern office workspace\",\\n      \"team collaboration\"\\n    ]\\n  }\\n}\\n```\\n",
    "return_code": 0,
    "status": "completed"
}

# Create manual execution with test data
print("\nOption 1: Test Extract URL node with mock Claude output")
print("-" * 40)

# Create a simplified test to just check the extraction
test_extraction_command = """echo '{}' | python3 -c "
import sys, json, re
data = sys.stdin.read()

# Try to parse as JSON first
try:
    parsed = json.loads(data)
    if 'output' in parsed:
        output = parsed['output']
        # Look for deployment_url in report
        match = re.search(r'\\\"deployment_url\\\"\\s*:\\s*\\\"([^\\\"]+)\\\"', output)
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

# Direct pattern matching
match = re.search(r'\\\"deployment_url\\\"\\s*:\\s*\\\"([^\\\"]+)\\\"', data)
if match:
    print(match.group(1))
    sys.exit(0)

match = re.search(r'https://[a-zA-Z0-9\\-]+\\.buildyoursite\\.pro', data)
if match:
    print(match.group(0))
else:
    print('URL_NOT_FOUND')
"
""".format(json.dumps(mock_claude_output).replace('"', '\\"'))

print("Testing extraction with mock Claude output...")
print(f"Mock output contains URL: https://test-company.buildyoursite.pro")

# Actually let's create a simpler direct test
print("\n" + "=" * 60)
print("DIRECT TEST OF EXTRACTION LOGIC")
print("=" * 60)

# Test different output formats
test_cases = [
    {
        "name": "Format 1: Direct URL + JSON report",
        "output": '{"error":null,"job_id":"8cc30903-4908-4ec5-8806-ed90be9ab6ae","output":"https://brader-wohnen.buildyoursite.pro\\n\\njson\\n{\\n  \\"report\\": {\\n    \\"deployment_url\\": \\"https://brader-wohnen.buildyoursite.pro\\"\\n  }\\n}\\n","return_code":0,"status":"completed"}'
    },
    {
        "name": "Format 2: JSON code block",
        "output": '{"error":null,"job_id":"15adc684-78f7-49fb-99d2-42fd2fe78737","output":"```json\\n{\\n  \\"report\\": {\\n    \\"deployment_url\\": \\"https://gasthof-hirsch.buildyoursite.pro\\"\\n  }\\n}\\n```\\n","return_code":0,"status":"completed"}'
    }
]

import re

for test in test_cases:
    print(f"\nTest: {test['name']}")
    print("-" * 40)

    data = test['output']

    # Method 1: Parse JSON and extract from output field
    try:
        parsed = json.loads(data)
        if 'output' in parsed:
            output = parsed['output']
            # Look for deployment_url
            match = re.search(r'"deployment_url"\s*:\s*"([^"]+)"', output)
            if match:
                print(f"✓ Found via deployment_url: {match.group(1)}")
            else:
                # Look for any buildyoursite.pro URL
                match = re.search(r'https://[a-zA-Z0-9\-]+\.buildyoursite\.pro', output)
                if match:
                    print(f"✓ Found via URL pattern: {match.group(0)}")
    except:
        print("✗ Failed to parse JSON")

print("\n" + "=" * 60)
print("CREATING TEST EXECUTION REQUEST")
print("=" * 60)

# Now let's create a manual execution with pinned data
execution_data = {
    "workflowData": {
        "nodes": workflow['nodes'],
        "connections": workflow['connections'],
        "settings": workflow.get('settings', {}),
        "staticData": workflow.get('staticData', {})
    },
    "startNodes": ["Extract website url"],  # Start from this node
    "runData": {
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

print("\nWould you like to:")
print("1. Execute the workflow with mock data via API")
print("2. See instructions for manual testing in the UI")
print("\nFor manual testing in the UI:")
print("-" * 60)
print("1. Go to: https://n8n.getmybot.pro/#/workflow/" + workflow_id)
print("2. Click on 'Deploy site to with Claude' node")
print("3. Click 'Pin' button in the output panel")
print("4. Set pinned output to:")
print(json.dumps({
    "stdout": json.dumps(mock_claude_output),
    "stderr": "",
    "returnCode": 0
}, indent=2))
print("5. Disable all nodes before 'Deploy site to with Claude'")
print("6. Execute workflow manually from 'Extract website url' node")
print("7. Check if URL is extracted correctly")

# Alternative: Test via webhook
print("\n" + "=" * 60)
print("ALTERNATIVE: Create test webhook workflow")
print("=" * 60)
print("We can also create a separate test workflow with:")
print("1. Webhook trigger (for easy testing)")
print("2. Set node with mock data")
print("3. Extract URL node with our extraction logic")
print("4. Response node to return the result")