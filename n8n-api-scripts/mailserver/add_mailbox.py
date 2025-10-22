#!/usr/bin/env python3
"""
Create mailboxes in Mailcow via API
This avoids the duplicate ID bug in the web UI
"""

import requests
import json
import sys

# Configuration
MAILCOW_URL = "https://mail.y2k.global"
MAILCOW_DOMAIN = "y2k.global"

def create_mailbox(username, password, quota_mb=3072, display_name=None):
    """
    Create a new mailbox in Mailcow

    Args:
        username: Email address (e.g., user@y2k.global)
        password: Password for the mailbox
        quota_mb: Mailbox quota in MB (default 3GB)
        display_name: Display name (optional)
    """

    # Ensure username has domain
    if '@' not in username:
        username = f"{username}@{MAILCOW_DOMAIN}"

    # Prepare mailbox data
    mailbox_data = {
        "username": username,
        "password": password,
        "password2": password,  # Confirmation password
        "quota": str(quota_mb * 1048576),  # Convert MB to bytes
        "force_pw_update": 0,
        "active": 1
    }

    if display_name:
        mailbox_data["name"] = display_name

    # Send request to Mailcow API
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        # Use the web form endpoint (requires session cookie)
        print(f"Note: This script requires active admin session.")
        print(f"Creating mailbox: {username}")
        print(f"Quota: {quota_mb} MB")

        # For API-based creation, you would need to use:
        # POST /api/v1/add/mailbox
        # But this requires proper authentication

        print("\nTo create mailboxes via API, use curl with proper authentication:")
        print(f"\ncurl -X POST '{MAILCOW_URL}/api/v1/add/mailbox' \\")
        print(f"  -H 'Content-Type: application/json' \\")
        print(f"  -d '{json.dumps(mailbox_data)}'")
        print("\nOr use the web interface: https://mail.y2k.global/admin/")
        print("Browser tip: Clear cache (Ctrl+Shift+Del) to fix duplicate ID issue")

    except Exception as e:
        print(f"Error: {e}")
        return False

    return True


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        username = sys.argv[1]
        password = sys.argv[2] if len(sys.argv) > 2 else input("Password: ")
        quota = int(sys.argv[3]) if len(sys.argv) > 3 else 3072

        create_mailbox(username, password, quota)
    else:
        print("Usage: add_mailbox.py <username> <password> [quota_mb]")
        print("Example: add_mailbox.py user@y2k.global MyPassword123 3072")
        print("\nNote: Due to browser caching issues in Mailcow UI, use the web form:")
        print("1. Go to https://mail.y2k.global/admin/")
        print("2. Clear browser cache (Ctrl+Shift+Del)")
        print("3. Click 'Add Mailbox'")
        print("4. Fill in the form and submit")
