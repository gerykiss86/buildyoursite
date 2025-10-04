"""Analyze specific execution to see Claude output format"""
import requests
import json
import os
import re
from dotenv import load_dotenv

load_dotenv('n8n.env')

base_url = os.getenv('N8N_URL')
api_key = os.getenv('N8N_API_KEY')

headers = {
    "Accept": "application/json",
    "X-N8N-API-KEY": api_key
}

# Check a recent successful execution
exec_ids = [287, 285, 282, 281, 278]  # Recent long-running executions

for exec_id in exec_ids[:3]:  # Check first 3
    print(f"\n{'='*80}")
    print(f"ANALYZING EXECUTION ID: {exec_id}")
    print('='*80)

    response = requests.get(
        f"{base_url}/api/v1/executions/{exec_id}",
        headers=headers
    )

    if response.status_code == 200:
        details = response.json()

        # Check if execution was successful
        if details.get('finished'):
            print("[SUCCESS] Execution finished successfully")
        else:
            print("[FAILED] Execution did not finish successfully")
            continue

        # Get the run data
        if 'data' in details and 'resultData' in details['data']:
            run_data = details['data']['resultData'].get('runData', {})

            # Find Claude deployment node
            claude_found = False
            for node_name, node_data in run_data.items():
                if 'Deploy site to with Claude' in node_name:
                    claude_found = True
                    print(f"\n[FOUND] Claude deployment node")

                    if node_data and len(node_data) > 0:
                        output = node_data[0].get('json', {})

                        if 'stdout' in output:
                            stdout = output['stdout']

                            # Save raw output
                            with open(f'exec_{exec_id}_claude_raw.txt', 'w', encoding='utf-8') as f:
                                f.write(stdout)

                            print(f"Saved raw output to: exec_{exec_id}_claude_raw.txt")

                            # Analyze output structure
                            print("\n[ANALYZING] Output structure:")
                            print("-" * 40)

                            # Check for JSON response
                            if stdout.strip().startswith('{'):
                                try:
                                    parsed = json.loads(stdout)
                                    print("Output is valid JSON:")
                                    print(json.dumps(parsed, indent=2)[:500])

                                    # Check different fields
                                    if 'output' in parsed:
                                        print(f"\n[OK] Has 'output' field: {parsed['output'][:100] if parsed['output'] else 'empty'}")
                                    if 'deploymentUrl' in parsed:
                                        print(f"[OK] Has 'deploymentUrl' field: {parsed['deploymentUrl']}")
                                    if 'deployment_url' in parsed:
                                        print(f"[OK] Has 'deployment_url' field: {parsed['deployment_url']}")
                                    if 'url' in parsed:
                                        print(f"[OK] Has 'url' field: {parsed['url']}")

                                except json.JSONDecodeError:
                                    print("Failed to parse as JSON, checking for embedded JSON...")

                            # Look for URLs in the output
                            urls = re.findall(r'https://[a-zA-Z0-9\-\.]+\.buildyoursite\.pro[^\s"\'<>]*', stdout)
                            if urls:
                                print(f"\n[URLS] Found buildyoursite.pro URLs:")
                                for url in set(urls):
                                    print(f"  - {url}")

                            # Check how the output field looks
                            output_matches = re.findall(r'"output"\s*:\s*"([^"]*)"', stdout)
                            if output_matches:
                                print(f"\n[OUTPUT] 'output' field contents:")
                                for match in output_matches[:3]:
                                    print(f"  - {match[:100]}")

                            # Check for deployment URL patterns
                            deployment_patterns = [
                                r'"deploymentUrl"\s*:\s*"([^"]*)"',
                                r'"deployment_url"\s*:\s*"([^"]*)"',
                                r'"url"\s*:\s*"(https://[^"]*)"'
                            ]

                            for pattern in deployment_patterns:
                                matches = re.findall(pattern, stdout)
                                if matches:
                                    print(f"\n[PATTERN] Found with pattern {pattern}:")
                                    for match in matches:
                                        print(f"  - {match}")

            # Check Extract URL node
            for node_name, node_data in run_data.items():
                if 'Extract website url' in node_name:
                    print(f"\n[EXTRACT] Extract URL node result:")

                    if node_data and len(node_data) > 0:
                        output = node_data[0].get('json', {})
                        if 'stdout' in output:
                            extracted = output['stdout']
                            print(f"  Extracted value: '{extracted[:200]}'")
                        if 'stderr' in output and output['stderr']:
                            print(f"  Error: {output['stderr']}")

            if not claude_found:
                print("\n[WARNING] Claude deployment node not found in this execution")

    else:
        print(f"Error fetching execution {exec_id}: {response.status_code}")