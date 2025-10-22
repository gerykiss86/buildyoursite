#!/usr/bin/env python3
"""
Test admin login with detailed debugging
"""

import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("=" * 60)
print("Testing Admin Login")
print("=" * 60)

base_url = "https://mail.y2k.global"
session = requests.Session()

# Step 1: Get the login page
print("\n1. Getting login page...")
response = session.get(f"{base_url}/", verify=False)
print(f"   Status: {response.status_code}")
print(f"   Cookies: {session.cookies.get_dict()}")

# Step 2: Check if we can see login form
if 'form' in response.text.lower() or 'login' in response.text.lower():
    print("   [OK] Login form found")
else:
    print("   [INFO] Response contains:", response.text[:200])

# Step 3: Try to login
print("\n2. Attempting login with admin/Admin2025!...")
login_payload = {
    'login_user': 'admin',
    'pass_user': 'Admin2025!'
}

response = session.post(
    f"{base_url}/",
    data=login_payload,
    verify=False,
    allow_redirects=False
)

print(f"   Status: {response.status_code}")
print(f"   Headers: {dict(response.headers)}")
print(f"   Cookies after login: {session.cookies.get_dict()}")

if response.status_code in [200, 302, 303]:
    print("   [OK] Login attempt sent")
else:
    print(f"   [WARN] Unexpected status code")

# Step 4: Try to access admin panel
print("\n3. Accessing admin panel...")
response = session.get(f"{base_url}/admin", verify=False)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    print("   [OK] Can access admin panel")
else:
    print(f"   [FAIL] Cannot access admin panel")
    print(f"   Response: {response.text[:300]}")

# Step 5: Try to access user panel
print("\n4. Accessing user panel...")
response = session.get(f"{base_url}/user", verify=False)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    print("   [OK] Can access user panel")
else:
    print(f"   [INFO] Status: {response.status_code}")

# Step 6: Check if we're authenticated by trying an API call
print("\n5. Testing API access (requires auth)...")
response = session.get(f"{base_url}/api/v1/get/status/version", verify=False)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    try:
        data = response.json()
        print(f"   [OK] API authenticated: {data}")
    except:
        print(f"   [INFO] API response: {response.text[:200]}")
else:
    print(f"   [FAIL] API not authenticated")

print("\n" + "=" * 60)
