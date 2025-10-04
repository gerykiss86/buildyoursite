#!/usr/bin/env python3
"""
Test script for Claude Execution Server
Can be run from Docker container or any machine with network access
"""

import requests
import json
import sys
import time

# Server configuration - update these based on your setup
SERVER_HOST = 'host.docker.internal'  # Use this from Docker, or use actual IP
SERVER_PORT = 5555
BASE_URL = f'http://{SERVER_HOST}:{SERVER_PORT}'

def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f'{BASE_URL}/health')
        if response.status_code == 200:
            print(f"✓ Health check passed: {response.json()}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Could not connect to server: {e}")
        return False

def test_simple_print():
    """Test simple print command"""
    print("\nTesting simple print command...")
    prompt = "Output only this text without using any tools: hello_from_claude"

    try:
        response = requests.post(
            f'{BASE_URL}/execute',
            json={'prompt': prompt},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Execute command successful:")
            print(f"  Status: {result.get('status')}")
            print(f"  Output: {result.get('output', '').strip()}")
            if result.get('error'):
                print(f"  Error: {result.get('error')}")
            return True
        else:
            print(f"✗ Execute command failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error executing command: {e}")
        return False

def test_streaming():
    """Test streaming response"""
    print("\nTesting streaming response...")
    prompt = "Output only this text without using any tools: Line 1\\nLine 2\\nLine 3"

    try:
        response = requests.post(
            f'{BASE_URL}/execute',
            json={'prompt': prompt, 'stream': True},
            stream=True,
            timeout=30
        )

        if response.status_code == 200:
            print("✓ Streaming response:")
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if data.get('output'):
                        print(f"  > {data['output']}")
                    if data.get('status') == 'completed':
                        print(f"  Status: completed")
            return True
        else:
            print(f"✗ Streaming failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error with streaming: {e}")
        return False

def test_async_execution():
    """Test async execution"""
    print("\nTesting async execution...")
    prompt = "Output only this text without using any tools: async_test_complete"

    try:
        # Start async job
        response = requests.post(
            f'{BASE_URL}/execute-async',
            json={'prompt': prompt},
            timeout=10
        )

        if response.status_code != 200:
            print(f"✗ Failed to start async job: {response.status_code}")
            return False

        job_data = response.json()
        job_id = job_data['job_id']
        print(f"✓ Job started: {job_id}")

        # Poll for completion
        max_attempts = 30
        for i in range(max_attempts):
            time.sleep(1)
            status_response = requests.get(f'{BASE_URL}/job/{job_id}')

            if status_response.status_code == 200:
                job_status = status_response.json()
                print(f"  Status: {job_status.get('status')}")

                if job_status.get('status') == 'completed':
                    print(f"✓ Async job completed:")
                    print(f"  Output: {job_status.get('output', '').strip()}")
                    return True
                elif job_status.get('status') == 'error':
                    print(f"✗ Job failed: {job_status.get('error')}")
                    return False
            else:
                print(f"✗ Failed to get job status: {status_response.status_code}")
                return False

        print(f"✗ Job timed out after {max_attempts} seconds")
        return False

    except Exception as e:
        print(f"✗ Error with async execution: {e}")
        return False

def test_deployment_prompt():
    """Test a deployment-style prompt"""
    print("\nTesting deployment prompt...")
    prompt = """Without using any tools, provide these deployment details:
    Project: test-project
    Deploy path: /var/www/skykey/test-demo
    Output only: https://test-demo.skykey.at"""

    try:
        response = requests.post(
            f'{BASE_URL}/execute',
            json={'prompt': prompt},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Deployment prompt successful:")
            print(f"  Output: {result.get('output', '').strip()}")
            return True
        else:
            print(f"✗ Deployment prompt failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error with deployment prompt: {e}")
        return False

def main():
    """Run all tests"""
    print(f"Testing Claude Execution Server at {BASE_URL}")
    print("=" * 50)

    # Check command line arguments for custom host
    if len(sys.argv) > 1:
        global SERVER_HOST, BASE_URL
        SERVER_HOST = sys.argv[1]
        BASE_URL = f'http://{SERVER_HOST}:{SERVER_PORT}'
        print(f"Using custom host: {SERVER_HOST}")

    tests = [
        ('Health Check', test_health),
        ('Simple Print', test_simple_print),
        ('Streaming', test_streaming),
        ('Async Execution', test_async_execution),
        ('Deployment Prompt', test_deployment_prompt)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ Test {test_name} crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    for test_name, success in results:
        status = "✓" if success else "✗"
        print(f"  {status} {test_name}")

    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")

    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())