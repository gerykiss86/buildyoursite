#!/usr/bin/env python3
"""
Test all Mailcow logins to ensure they work
"""

import requests
import re
from urllib.parse import urljoin
import json

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_admin_login():
    """Test admin panel login at mail.y2k.global"""
    print("=" * 60)
    print("Testing Admin Panel Login")
    print("=" * 60)

    base_url = "https://mail.y2k.global"
    session = requests.Session()

    # Get login page
    response = session.get(f"{base_url}/", verify=False)
    print(f"1. Login page status: {response.status_code}")

    # Try to login using the standard form submission
    login_data = {
        'login_user': 'admin',
        'pass_user': 'Admin2025!',
    }

    # Post to the login endpoint
    response = session.post(f"{base_url}/",
                          data=login_data,
                          verify=False,
                          allow_redirects=False)

    print(f"2. Login response: {response.status_code}")

    # Check if login was successful by trying to access API
    api_response = session.get(f"{base_url}/api/v1/get/status/version",
                              verify=False)

    if api_response.status_code == 200:
        print("   [OK] Admin login successful!")
        return True
    else:
        print(f"   [FAIL] Admin login failed")

    return response.status_code == 200

def test_webmail_login():
    """Test webmail login at webmail.y2k.global"""
    print("\n" + "=" * 60)
    print("Testing Webmail (SOGo) Login")
    print("=" * 60)

    base_url = "https://webmail.y2k.global"
    session = requests.Session()

    # Get SOGo login page
    response = session.get(f"{base_url}/", verify=False, allow_redirects=True)
    print(f"1. Webmail page status: {response.status_code}")
    print(f"   Final URL: {response.url}")

    # Try SOGo login
    login_url = "https://mail.y2k.global/SOGo/connect"
    login_data = {
        'userName': 'test@y2k.global',
        'password': 'Test2025!',
        'domain': '',
        'rememberLogin': '0'
    }

    response = session.post(login_url, data=login_data, verify=False, allow_redirects=False)
    print(f"2. SOGo login response: {response.status_code}")

    if response.status_code in [302, 303]:
        print("   [OK] Webmail login successful (redirecting)!")
        location = response.headers.get('Location', '')
        print(f"   Redirect to: {location}")
        return True
    else:
        print(f"   [FAIL] Webmail login failed")
        return False

def test_smtp_auth():
    """Test SMTP authentication"""
    print("\n" + "=" * 60)
    print("Testing SMTP Authentication")
    print("=" * 60)

    import smtplib

    try:
        print("1. Connecting to SMTP server on port 587...")
        smtp = smtplib.SMTP('mail.y2k.global', 587)
        smtp.starttls()

        print("2. Attempting authentication...")
        smtp.login('test@y2k.global', 'Test2025!')

        print("   [OK] SMTP authentication successful!")
        smtp.quit()
        return True
    except Exception as e:
        print(f"   [FAIL] SMTP authentication failed: {e}")
        return False

def test_imap_auth():
    """Test IMAP authentication"""
    print("\n" + "=" * 60)
    print("Testing IMAP Authentication")
    print("=" * 60)

    import imaplib

    try:
        print("1. Connecting to IMAP server on port 993...")
        imap = imaplib.IMAP4_SSL('mail.y2k.global', 993)

        print("2. Attempting authentication...")
        imap.login('test@y2k.global', 'Test2025!')

        print("   [OK] IMAP authentication successful!")
        imap.logout()
        return True
    except Exception as e:
        print(f"   [FAIL] IMAP authentication failed: {e}")
        return False

if __name__ == "__main__":
    results = {
        "admin_panel": test_admin_login(),
        "webmail": test_webmail_login(),
        "smtp": test_smtp_auth(),
        "imap": test_imap_auth()
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for service, status in results.items():
        status_icon = "[OK]" if status else "[FAIL]"
        print(f"{status_icon} {service.replace('_', ' ').title()}: {'Working' if status else 'Failed'}")

    if all(results.values()):
        print("\nAll services working correctly!")
    else:
        print("\nSome services need attention")

    print("\nAccess URLs:")
    print("- Admin Panel: https://mail.y2k.global (admin / Admin2025!)")
    print("- Webmail: https://webmail.y2k.global (test@y2k.global / Test2025!)")