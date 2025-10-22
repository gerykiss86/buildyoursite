#!/usr/bin/env python3
"""
Test webmail login with the new mailbox
"""

import requests

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("=" * 60)
print("Testing Webmail Login with New Mailbox")
print("=" * 60)

base_url = "https://webmail.y2k.global"
session = requests.Session()

# Get webmail page
response = session.get(f"{base_url}/", verify=False, allow_redirects=True)
print(f"1. Webmail page status: {response.status_code}")
print(f"   Final URL: {response.url}")

# Try SOGo login
login_url = "https://mail.y2k.global/SOGo/connect"
login_data = {
    'userName': 'newtest@y2k.global',
    'password': 'NewTest2025!',
    'domain': '',
    'rememberLogin': '0'
}

response = session.post(login_url, data=login_data, verify=False, allow_redirects=False)
print(f"2. SOGo login response: {response.status_code}")

if response.status_code in [302, 303]:
    print("   [OK] Webmail login successful!")
    location = response.headers.get('Location', '')
    print(f"   Redirect to: {location}")
else:
    print(f"   [FAIL] Webmail login failed")
    print(f"   Response headers: {dict(response.headers)}")

print("=" * 60)