#!/usr/bin/env python3
"""
Deploy Telegram Bot to Linux Server
Uses plink to transfer files and start the bot on the remote server
"""

import subprocess
import os
import sys
from pathlib import Path

# Configuration
SSH_KEY = r"C:\temp\ssh\waywiser\private.ppk"
SERVER_HOST = "82.165.141.243"
SERVER_USER = "root"
REMOTE_BOT_DIR = "/root/telegram-bot"
LOCAL_BOT_DIR = Path(__file__).parent

def run_plink_command(command, description=""):
    """Run a command via plink and return the result"""
    full_command = [
        "plink",
        "-i", SSH_KEY,
        f"{SERVER_USER}@{SERVER_HOST}",
        command
    ]

    print(f"\n{'=' * 60}")
    if description:
        print(f"📡 {description}")
    print(f"Command: {command}")
    print('=' * 60)

    try:
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.stdout:
            print(f"✓ Output:\n{result.stdout}")
        if result.stderr:
            print(f"⚠ Stderr:\n{result.stderr}")

        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print("✗ Command timed out")
        return False, "", "Timeout"
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False, "", str(e)

def upload_file(local_path, remote_path, description=""):
    """Upload a file using pscp"""
    print(f"\n{'=' * 60}")
    if description:
        print(f"📤 {description}")
    print(f"Uploading: {local_path} -> {remote_path}")
    print('=' * 60)

    try:
        result = subprocess.run(
            [
                "pscp",
                "-i", SSH_KEY,
                local_path,
                f"{SERVER_USER}@{SERVER_HOST}:{remote_path}"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print("✓ Upload successful")
            return True
        else:
            print(f"✗ Upload failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def main():
    print("\n" + "=" * 60)
    print("🤖 Telegram Bot Deployment to Linux Server")
    print("=" * 60)
    print(f"Target: {SERVER_USER}@{SERVER_HOST}")
    print(f"Remote Directory: {REMOTE_BOT_DIR}")
    print(f"Local Directory: {LOCAL_BOT_DIR}")

    # Check if SSH key exists
    if not os.path.exists(SSH_KEY):
        print(f"\n✗ Error: SSH key not found at {SSH_KEY}")
        sys.exit(1)

    print(f"✓ SSH key found: {SSH_KEY}")

    # Step 1: Test connection
    print("\n\n" + "=" * 60)
    print("STEP 1: Testing SSH Connection")
    print("=" * 60)

    success, stdout, stderr = run_plink_command(
        "echo 'SSH connection successful'",
        "Testing SSH connection"
    )

    if not success:
        print("\n✗ SSH connection failed!")
        sys.exit(1)

    # Step 2: Create remote directory
    print("\n\nSTEP 2: Creating Remote Directory")
    run_plink_command(
        f"mkdir -p {REMOTE_BOT_DIR}",
        "Creating remote bot directory"
    )

    # Step 3: Upload bot files
    print("\n\nSTEP 3: Uploading Bot Files")

    files_to_upload = [
        ("telegram-bot-linux.py", "Bot main script"),
        (".env", "Configuration file"),
    ]

    for filename, description in files_to_upload:
        local_path = LOCAL_BOT_DIR / filename
        if local_path.exists():
            remote_path = f"{REMOTE_BOT_DIR}/{filename}"
            upload_file(str(local_path), remote_path, description)
        else:
            print(f"⚠ Warning: {filename} not found at {local_path}")

    # Step 4: Make bot executable
    print("\n\nSTEP 4: Setting Permissions")
    run_plink_command(
        f"chmod +x {REMOTE_BOT_DIR}/telegram-bot-linux.py",
        "Making bot script executable"
    )

    # Step 5: Check dependencies
    print("\n\nSTEP 5: Checking Dependencies")
    run_plink_command(
        "python3 --version",
        "Checking Python installation"
    )

    run_plink_command(
        "pip3 show requests",
        "Checking requests library"
    )

    # Step 6: Test Claude Execution Server connectivity
    print("\n\nSTEP 6: Testing Claude Execution Server")
    run_plink_command(
        "curl -s http://localhost:5555/health | python3 -m json.tool || echo 'Server not responding'",
        "Testing Claude Execution Server on port 5555"
    )

    # Step 7: Create systemd service
    print("\n\nSTEP 7: Creating Systemd Service")

    service_content = f'''[Unit]
Description=BuildYourSite Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory={REMOTE_BOT_DIR}
ExecStart=/usr/bin/python3 {REMOTE_BOT_DIR}/telegram-bot-linux.py
Restart=always
RestartSec=10
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
'''

    # Escape the service content for the echo command
    escaped_content = service_content.replace('"', '\\"').replace('\n', '\\n')

    run_plink_command(
        f'echo -e "{escaped_content}" > /etc/systemd/system/telegram-bot.service',
        "Creating systemd service file"
    )

    # Reload systemd
    run_plink_command(
        "systemctl daemon-reload",
        "Reloading systemd daemon"
    )

    # Step 8: Start the bot
    print("\n\nSTEP 8: Starting Telegram Bot Service")
    run_plink_command(
        "systemctl start telegram-bot",
        "Starting telegram-bot service"
    )

    # Step 9: Enable service on boot
    run_plink_command(
        "systemctl enable telegram-bot",
        "Enabling telegram-bot service on boot"
    )

    # Step 10: Check service status
    print("\n\nSTEP 10: Checking Service Status")
    run_plink_command(
        "systemctl status telegram-bot",
        "Checking telegram-bot service status"
    )

    # Step 11: View logs
    print("\n\nSTEP 11: Viewing Bot Logs")
    run_plink_command(
        "journalctl -u telegram-bot -n 20 --no-pager",
        "Last 20 lines of bot logs"
    )

    print("\n\n" + "=" * 60)
    print("✓ Deployment Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check service status: systemctl status telegram-bot")
    print("2. View logs: journalctl -u telegram-bot -f")
    print("3. Stop bot: systemctl stop telegram-bot")
    print("4. Restart bot: systemctl restart telegram-bot")
    print("\nThe bot is now running on the Linux server!")
    print(f"Test by sending a message to @BuildYourSiteProBot on Telegram")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
