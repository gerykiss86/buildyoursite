#!/usr/bin/env python3
"""
Telegram Bot for Linux Server
Connects to Claude Execution Server (port 5555) for Claude command execution
This bot echoes back messages or executes Claude prompts via the execution server

Usage:
1. Create a .env file with: BOT_TOKEN=your_token_here
2. Make sure the Claude Execution Server is running on port 5555
3. Run: python3 telegram-bot-linux.py
4. Send messages to @BuildYourSiteProBot on Telegram
"""

import requests
import os
import time
from datetime import datetime
import json

# Load .env file
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        raise FileNotFoundError('.env file not found')

    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    return env_vars

env_vars = load_env()
BOT_TOKEN = env_vars.get('BOT_TOKEN')
CLAUDE_SERVER_URL = env_vars.get('CLAUDE_SERVER_URL', 'http://localhost:5555')

if not BOT_TOKEN:
    print("Error: BOT_TOKEN not found in .env file")
    exit(1)

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# Load allowed users whitelist
def load_allowed_users():
    """Load allowed users from JSON file"""
    try:
        allowed_users_path = os.path.join(os.path.dirname(__file__), 'allowed_users.json')
        with open(allowed_users_path, 'r') as f:
            data = json.load(f)
        allowed_ids = {user['id']: user for user in data.get('allowed_users', [])}
        print(f"✓ Loaded {len(allowed_ids)} allowed users from whitelist")
        return allowed_ids
    except FileNotFoundError:
        print("⚠ Warning: allowed_users.json not found. Access control disabled.")
        return {}
    except json.JSONDecodeError:
        print("⚠ Warning: allowed_users.json is invalid JSON. Access control disabled.")
        return {}


def is_user_allowed(user_id, allowed_users):
    """Check if user is in whitelist"""
    if not allowed_users:  # If no whitelist, allow everyone
        return True
    return user_id in allowed_users


# Load whitelist at startup
ALLOWED_USERS = load_allowed_users()


def make_request(method, params=None):
    """Make HTTP request to Telegram API"""
    if params is None:
        params = {}

    try:
        url = f"{BASE_URL}/{method}"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if not data.get('ok'):
            raise Exception(f"Telegram API error: {data.get('description', 'Unknown error')}")

        return data.get('result')

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {str(e)}")
    except ValueError as e:
        raise Exception(f"JSON parsing error: {str(e)}")


def send_message(chat_id, text):
    """Send a message to a chat"""
    try:
        result = make_request('sendMessage', {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        })
        print(f"✓ Message sent to chat {chat_id}")
        return result
    except Exception as error:
        print(f"✗ Failed to send message: {str(error)}")


def get_updates(offset=0):
    """Get updates from Telegram (polling)"""
    try:
        updates = make_request('getUpdates', {
            'offset': offset,
            'timeout': 30
        })
        return updates if updates else []
    except Exception as error:
        print(f"Error getting updates: {str(error)}")
        return []


def execute_claude_command(prompt):
    """Execute a Claude command via the execution server"""
    try:
        response = requests.post(
            f"{CLAUDE_SERVER_URL}/execute",
            json={'prompt': prompt, 'stream': False},
            timeout=300  # 5 minute timeout for Claude execution
        )
        response.raise_for_status()

        result = response.json()

        if result.get('status') == 'error':
            raise Exception(result.get('error', 'Unknown error from execution server'))

        if result.get('return_code') != 0:
            error_msg = result.get('error', 'Command returned non-zero exit code')
            raise Exception(error_msg)

        return result.get('output', '')

    except requests.exceptions.ConnectionError:
        raise Exception(f"Cannot connect to Claude Execution Server at {CLAUDE_SERVER_URL}:5555. Make sure it's running.")
    except requests.exceptions.Timeout:
        raise Exception("Claude Execution Server request timed out (5 minutes)")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {str(e)}")
    except Exception as e:
        raise e


def escape_html(text):
    """Escape HTML special characters for Telegram"""
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    }
    for char, escaped in replacements.items():
        text = text.replace(char, escaped)
    return text


def handle_update(update):
    """Process incoming updates"""
    if 'message' not in update:
        return

    message = update['message']
    chat_id = message['chat']['id']
    user_id = message['from']['id']
    user_name = message['from'].get('first_name', 'Unknown')
    text = message.get('text', '')

    if not text:
        return

    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"\n[{timestamp}] Message from {user_name} (ID: {user_id})")
    print(f"Chat ID: {chat_id}")
    print(f"Text: \"{text}\"")

    # Check if user is allowed (access control)
    if not is_user_allowed(user_id, ALLOWED_USERS):
        send_message(chat_id, '❌ Access denied. You are not authorized to use this bot.')
        print(f"⛔ Unauthorized access attempt by {user_name} (ID: {user_id})")
        return

    # Check if message starts with "claude:"
    if text.lower().startswith('claude:'):
        prompt = text[7:].strip()  # Remove "claude:" prefix

        if not prompt:
            send_message(chat_id, 'Error: Please provide a prompt after "claude:"')
            return

        print(f"\n⚡ Executing Claude command: \"{prompt}\"")
        send_message(chat_id, '⏳ Processing Claude command via execution server...')

        try:
            result = execute_claude_command(prompt)
            response = f"<b>Claude Response:</b>\n\n<code>{escape_html(result)}</code>"

            # Split into chunks if too long (Telegram max is 4096 chars)
            if len(response) > 4000:
                chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
                for chunk in chunks:
                    send_message(chat_id, chunk)
            else:
                send_message(chat_id, response)

            print('✓ Claude command completed successfully')
        except Exception as error:
            response = f"<b>Error executing Claude command:</b>\n<code>{escape_html(str(error))}</code>"
            send_message(chat_id, response)
            print(f"✗ Claude command failed: {str(error)}")
    else:
        # Echo the message back
        response = f"Echo: {text}"
        send_message(chat_id, response)


def start_bot():
    """Main polling loop"""
    print("🤖 BuildYourSiteProBot (Linux) started!")
    print("📡 Polling for updates every second...")
    print(f"🔗 Bot URL: https://t.me/BuildYourSiteProBot")
    print(f"🖥️  Claude Server: {CLAUDE_SERVER_URL}")
    if ALLOWED_USERS:
        print(f"🔒 Access Control: Enabled ({len(ALLOWED_USERS)} authorized users)")
    else:
        print("🔓 Access Control: Disabled (all users allowed)\n")

    # Test the bot connection
    try:
        me = make_request('getMe')
        print(f"✓ Connected as: @{me.get('username', 'Unknown')}")
        print(f"✓ Bot ID: {me.get('id', 'Unknown')}\n")
    except Exception as error:
        print(f"✗ Failed to connect to Telegram: {str(error)}")
        print("Please check your BOT_TOKEN")
        exit(1)

    # Test connection to Claude Execution Server
    try:
        response = requests.get(f"{CLAUDE_SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✓ Claude Execution Server is running on {CLAUDE_SERVER_URL}\n")
        else:
            print(f"⚠ Claude Execution Server returned status {response.status_code}\n")
    except Exception as error:
        print(f"⚠ Warning: Cannot connect to Claude Execution Server at {CLAUDE_SERVER_URL}")
        print(f"  Claude commands will fail until the server is available\n")

    last_update_id = 0

    # Polling loop
    try:
        while True:
            try:
                updates = get_updates(last_update_id + 1)

                for update in updates:
                    last_update_id = max(last_update_id, update.get('update_id', 0))
                    handle_update(update)

            except Exception as error:
                print(f"Error in polling loop: {str(error)}")

            time.sleep(1)  # Check for updates every second

    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped")
        exit(0)


if __name__ == "__main__":
    try:
        start_bot()
    except Exception as error:
        print(f"Fatal error: {error}")
        exit(1)
