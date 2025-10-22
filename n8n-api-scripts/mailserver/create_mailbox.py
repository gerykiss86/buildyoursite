#!/usr/bin/env python3
"""
Create a new mailbox using Mailcow API
"""

import requests
import json

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_url = "https://mail.y2k.global/api/v1/add/mailbox"
api_key = "y2k-mailcow-2025-api-key"

data = {
    "local_part": "newtest",
    "domain": "y2k.global",
    "name": "New Test User",
    "quota": 5120,
    "password": "NewTest2025!",
    "password2": "NewTest2025!",
    "active": 1
}

headers = {
    "X-API-Key": api_key,
    "Content-Type": "application/json"
}

response = requests.post(api_url, json=data, headers=headers, verify=False)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    result = response.json()
    if result[0].get('type') == 'success':
        print("\n[OK] Mailbox created successfully!")
        print(f"Email: newtest@y2k.global")
        print(f"Password: NewTest2025!")
    else:
        print(f"\n[FAIL] {result}")
else:
    print(f"\n[FAIL] API request failed")