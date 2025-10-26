#!/usr/bin/env python3
"""
Simple Echo Bot for Telegram
This bot echoes back any message it receives

Usage:
1. Create a .env file with: BOT_TOKEN=your_token_here
2. Run: python3 echo-bot.py
3. Send a message to @BuildYourSiteProBot on Telegram
"""

import requests
import os
import time
from datetime import datetime

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

if not BOT_TOKEN:
    print("Error: BOT_TOKEN not found in .env file")
    exit(1)

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


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
    """Execute a Claude command and return the result"""
    import subprocess
    import shutil

    # Try to find claude in common locations
    claude_paths = [
        'claude',  # In PATH
        r'C:\Users\info\AppData\Roaming\npm\claude',  # Windows npm global
        r'C:\Users\info\AppData\Roaming\npm\claude.cmd',  # Windows npm global (cmd)
        shutil.which('claude'),  # Find in PATH
    ]

    claude_cmd = None
    for path in claude_paths:
        if path and shutil.which(path) if '\\' not in path else True:
            if '\\' in path:
                # Direct path
                if subprocess.run(['cmd', '/c', f'where {path}'], capture_output=True).returncode == 0:
                    claude_cmd = path
                    break
            else:
                # Search in PATH
                if shutil.which(path):
                    claude_cmd = path
                    break

    if not claude_cmd:
        # Fallback to direct path
        claude_cmd = r'C:\Users\info\AppData\Roaming\npm\claude'

    try:
        result = subprocess.run(
            [claude_cmd, '--dangerously-skip-permissions', '--print', prompt],
            capture_output=True,
            text=True,
            timeout=60,
            shell=True
        )

        if result.returncode != 0:
            raise Exception(f"Claude command failed: {result.stderr}")

        return result.stdout
    except subprocess.TimeoutExpired:
        raise Exception("Claude command timed out (60 seconds)")
    except Exception as e:
        raise Exception(f"Failed to execute Claude: {str(e)}")


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

    # Check if message starts with "claude:"
    if text.lower().startswith('claude:'):
        prompt = text[7:].strip()  # Remove "claude:" prefix

        if not prompt:
            send_message(chat_id, 'Error: Please provide a prompt after "claude:"')
            return

        print(f"\n⚡ Executing Claude command: \"{prompt}\"")
        send_message(chat_id, '⏳ Processing Claude command...')

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
    print("🤖 BuildYourSiteProBot started!")
    print("📡 Polling for updates every second...")
    print("🔗 Bot URL: https://t.me/BuildYourSiteProBot\n")

    # Test the bot connection
    try:
        me = make_request('getMe')
        print(f"✓ Connected as: @{me.get('username', 'Unknown')}")
        print(f"✓ Bot ID: {me.get('id', 'Unknown')}\n")
    except Exception as error:
        print(f"✗ Failed to connect to Telegram: {str(error)}")
        print("Please check your BOT_TOKEN")
        exit(1)

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
