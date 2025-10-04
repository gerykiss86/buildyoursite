#!/usr/bin/env python3
import subprocess
import json

def execute_command(prompt, stream=False):
    command = [
        'su', '-', 'clauderunner', '-c',
        f'claude --dangerously-skip-permissions "{prompt}"'
    ]

    if stream:
        # This would be a generator
        def gen():
            yield "test"
        return gen()
    else:
        # This should be a dict
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=300
        )

        return {
            'job_id': 'test',
            'status': 'completed',
            'output': result.stdout,
            'error': result.stderr if result.stderr else None,
            'return_code': result.returncode
        }

# Test
result = execute_command("Output only: test", stream=False)
print(f"Type: {type(result)}")
print(f"Result: {result}")

try:
    json.dumps(result)
    print("JSON serialization: OK")
except Exception as e:
    print(f"JSON serialization error: {e}")