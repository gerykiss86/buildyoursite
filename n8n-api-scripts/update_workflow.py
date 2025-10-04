"""Update the workflow to properly extract URLs from Claude output"""
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
    "Content-Type": "application/json",
    "X-N8N-API-KEY": api_key
}

print("Fetching current workflow configuration...")
response = requests.get(f"{base_url}/api/v1/workflows/{workflow_id}", headers=headers)

if response.status_code != 200:
    print(f"Error fetching workflow: {response.status_code}")
    exit(1)

workflow = response.json()

# Find and update the Extract website url node
updated = False
for node in workflow['nodes']:
    if node['name'] == 'Extract website url':
        print(f"Found Extract URL node: {node['id']}")
        print(f"Current command: {node['parameters']['command']}")

        # Update the extraction command to handle both formats
        # This command will:
        # 1. First try to extract deployment_url from the JSON report
        # 2. If not found, extract any buildyoursite.pro URL
        # 3. Handle both direct output and JSON code block formats

        new_command = """={{
  // Get the stdout from previous node
  const output = $json.stdout || '';

  // First try to parse as JSON and get deployment_url
  try {
    const parsed = JSON.parse(output);
    if (parsed.output) {
      // Check if there's a deployment_url in the report
      const reportMatch = parsed.output.match(/"deployment_url"\\s*:\\s*"([^"]+)"/);
      if (reportMatch) {
        return reportMatch[1];
      }

      // Otherwise look for any buildyoursite.pro URL in the output
      const urlMatch = parsed.output.match(/https:\\/\\/[a-zA-Z0-9\\-]+\\.buildyoursite\\.pro/);
      if (urlMatch) {
        return urlMatch[0];
      }
    }
  } catch(e) {
    // Not valid JSON, continue with pattern matching
  }

  // Try to find deployment_url in JSON report (handles both formats)
  const deploymentUrlMatch = output.match(/"deployment_url"\\s*:\\s*"([^"]+)"/);
  if (deploymentUrlMatch) {
    return deploymentUrlMatch[1];
  }

  // Fallback: Find any buildyoursite.pro URL
  const urlMatch = output.match(/https:\\/\\/[a-zA-Z0-9\\-]+\\.buildyoursite\\.pro/);
  if (urlMatch) {
    return urlMatch[0];
  }

  return 'URL_NOT_FOUND';
}}"""

        node['parameters']['command'] = new_command
        updated = True
        print(f"Updated extraction command")
        break

if not updated:
    print("Extract website url node not found!")
    exit(1)

# Also update the Claude deployment node to ensure consistent output
for node in workflow['nodes']:
    if node['name'] == 'Deploy site to with Claude':
        print(f"\nFound Claude deployment node: {node['id']}")

        # Update the Claude prompt to be more explicit about output format
        current_command = node['parameters']['command']

        # Modify the prompt to ensure consistent output
        updated_prompt = current_command.replace(
            '8) Output ONLY the final deployment URL in format https://subfolder.buildyoursite.pro with no extra text.',
            '8) Output the final deployment URL at the very beginning of your response in format https://subfolder.buildyoursite.pro on its own line.'
        )

        updated_prompt = updated_prompt.replace(
            '9) After that, append an additional structured JSON block',
            '9) After the URL, append a structured JSON block'
        )

        node['parameters']['command'] = updated_prompt
        print("Updated Claude deployment prompt for consistent output")
        break

print("\nSaving updated workflow...")

# Update the workflow
update_response = requests.put(
    f"{base_url}/api/v1/workflows/{workflow_id}",
    headers=headers,
    json=workflow
)

if update_response.status_code == 200:
    print("[SUCCESS] Workflow updated successfully!")

    # Ensure workflow is active
    activate_response = requests.patch(
        f"{base_url}/api/v1/workflows/{workflow_id}",
        headers=headers,
        json={"active": True}
    )

    if activate_response.status_code == 200:
        print("[SUCCESS] Workflow is active and ready to use")
    else:
        print(f"[WARNING] Could not activate workflow: {activate_response.status_code}")
else:
    print(f"[ERROR] Failed to update workflow: {update_response.status_code}")
    print(update_response.text)