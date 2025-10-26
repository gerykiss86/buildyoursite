# Whitelist Management - User IDs vs Usernames

## Quick Answer

**You need Telegram User ID, not username.** However, you can manage it easily, and there are ways to find your ID.

---

## Why User IDs Instead of Usernames?

| Aspect | User ID | Username |
|--------|---------|----------|
| **Format** | Numeric (5092208953) | Text (@gergo) |
| **Reliability** | Always exists, never changes | Optional, can change |
| **Speed** | Direct lookup (no API call) | Requires API lookup |
| **Uniqueness** | Always unique | Not all users have one |
| **Bot Access** | Available from message | Not always available |
| **Security** | Harder to guess | Public/easy to discover |

**Telegram's recommendation**: Use User IDs for access control

---

## Method 1: Find Your ID Using @userinfobot (Easiest)

### Steps:
1. Open Telegram
2. Search for **`@userinfobot`**
3. Start the bot (send `/start`)
4. Send any message
5. Bot responds with your User ID

### Example Response:
```
Your user id: 5092208953
Your first name: Gergo
Your last name: Kiss
Your username: @gergokiss
Your language: en
```

✓ **Fastest way** - Takes 10 seconds!

---

## Method 2: Check Your User ID in @BuildYourSiteProBot Logs

When you send a message to your bot, the logs show your user ID:

```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 20"
```

Look for output like:
```
[22:33:50] Message from Gergo (ID: 5092208953)
Chat ID: 5092208953
Text: "hi"
```

Your **User ID is 5092208953** in this example.

✓ **Already works** - No extra tools needed

---

## Method 3: Get User IDs from Bot Messages

When someone sends a message to your bot, you can see their ID in the bot code:

```python
def handle_update(update):
    message = update['message']
    user_id = message['from']['id']              # ← This is their User ID
    username = message['from'].get('username')   # ← This is their @username (optional)

    print(f"User ID: {user_id}, Username: {username}")
```

---

## Method 4: Group/Channel User IDs

For group or channel IDs, use `@userinfobot` in the group:

1. Add `@userinfobot` to your group
2. Send `/start`
3. Bot shows group ID (negative number like `-1001234567890`)

---

## Managing the Whitelist - Best Practices

### Option A: Start Simple (Recommended)

Create `allowed_users.json`:

```json
{
  "allowed_users": [
    {"id": 5092208953, "name": "Gergo", "role": "admin"},
    {"id": 123456789, "name": "Friend", "role": "user"}
  ]
}
```

**To add a new user:**
1. Get their User ID (using @userinfobot)
2. Edit `allowed_users.json`
3. Add new entry with their ID and name
4. Upload to server:
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" allowed_users.json root@82.165.141.243:/root/telegram-bot/allowed_users.json
```
5. Restart bot:
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 restart telegram-bot"
```

### Option B: Support Both ID and Username

You can support **both User ID and username** if needed:

```python
import json

def load_allowed_users():
    """Load allowed users from JSON"""
    try:
        with open('allowed_users.json', 'r') as f:
            data = json.load(f)
        users_by_id = {}
        users_by_username = {}

        for user in data['allowed_users']:
            # Index by ID
            users_by_id[user['id']] = user
            # Index by username (if provided)
            if 'username' in user:
                users_by_username[user['username'].lower()] = user

        return users_by_id, users_by_username
    except FileNotFoundError:
        return {}, {}

ALLOWED_USERS_BY_ID, ALLOWED_USERS_BY_USERNAME = load_allowed_users()

def is_user_allowed(user_id, username=None):
    """Check if user is allowed by ID or username"""
    # Check by ID (fast)
    if user_id in ALLOWED_USERS_BY_ID:
        return True

    # Check by username (if provided)
    if username:
        username_lower = username.lower().lstrip('@')  # Remove @ if present
        if username_lower in ALLOWED_USERS_BY_USERNAME:
            return True

    return False

def handle_update(update):
    """Process incoming updates"""
    # ... existing code ...

    user_id = message['from']['id']
    username = message['from'].get('username', '')

    # Check access
    if not is_user_allowed(user_id, username):
        send_message(chat_id, '❌ Access denied.')
        return

    # ... rest of code ...
```

**JSON format for this approach:**
```json
{
  "allowed_users": [
    {
      "id": 5092208953,
      "name": "Gergo",
      "username": "gergokiss",
      "role": "admin"
    },
    {
      "id": 123456789,
      "name": "Friend",
      "username": "friend_name",
      "role": "user"
    }
  ]
}
```

---

## Whitelist Management Workflow

### Adding a New User

**Step 1: Get their User ID**
```
Ask them to send a message to @userinfobot
They get their ID
```

**Step 2: Update whitelist file**
```json
{
  "allowed_users": [
    {"id": 5092208953, "name": "Gergo", "role": "admin"},
    {"id": 987654321, "name": "New User", "role": "user"}  // ← NEW
  ]
}
```

**Step 3: Deploy to server**
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" allowed_users.json root@82.165.141.243:/root/telegram-bot/allowed_users.json
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 restart telegram-bot"
```

**Step 4: Verify**
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 10"
```

---

## Quick Reference: Finding Your User ID

| Method | Time | Difficulty | Result |
|--------|------|-----------|--------|
| @userinfobot | 10s | Easy | Immediate ID |
| Send message to bot | Instant | Easy | See in logs |
| API lookup | ~5s | Medium | Requires API call |
| Telegram Settings | 30s | Easy | Shows some info |

---

## User ID Examples

### Individual Users
```
Gergo: 5092208953
Friend: 123456789
```

### Group/Channels (Negative IDs)
```
Group: -1001234567890
Channel: -100987654321
```

### Special IDs
```
Anonymous: -1
Deleted Account: 777000
```

---

## Implementation Ready Code

Here's the complete implementation for Option A (JSON-based whitelist):

### Step 1: Create `allowed_users.json`

```json
{
  "allowed_users": [
    {
      "id": 5092208953,
      "name": "Gergo",
      "role": "admin",
      "allowed_commands": ["echo", "claude"],
      "added_date": "2025-10-25"
    }
  ]
}
```

### Step 2: Add to telegram-bot-linux.py

Add these functions at the top after imports:

```python
import json

# Load allowed users at startup
def load_allowed_users():
    """Load allowed users from JSON file"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'allowed_users.json'), 'r') as f:
            data = json.load(f)
        allowed_ids = {user['id']: user for user in data.get('allowed_users', [])}
        print(f"✓ Loaded {len(allowed_ids)} allowed users")
        return allowed_ids
    except FileNotFoundError:
        print("⚠ Warning: allowed_users.json not found. Access control disabled.")
        return {}
    except json.JSONDecodeError:
        print("⚠ Warning: allowed_users.json is invalid JSON. Access control disabled.")
        return {}

def is_user_allowed(user_id, allowed_users):
    """Check if user is in whitelist"""
    return user_id in allowed_users

# Load whitelist at startup
ALLOWED_USERS = load_allowed_users()

# Then in handle_update function, add this check right after getting user_id:

def handle_update(update):
    """Process incoming updates"""
    if 'message' not in update:
        return

    message = update['message']
    chat_id = message['chat']['id']
    user_id = message['from']['id']
    user_name = message['from'].get('first_name', 'Unknown')
    text = message.get('text', '')

    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"\n[{timestamp}] Message from {user_name} (ID: {user_id})")
    print(f"Chat ID: {chat_id}")
    print(f"Text: \"{text}\"")

    # NEW: Check if user is allowed
    if ALLOWED_USERS and not is_user_allowed(user_id, ALLOWED_USERS):
        send_message(chat_id, '❌ Access denied. You are not authorized to use this bot.')
        print(f"⛔ Unauthorized access attempt by {user_name} (ID: {user_id})")
        return

    # Rest of the code continues as normal...
    if text.lower().startswith('claude:'):
        # ... rest of code
```

### Step 3: Deploy

```bash
# 1. Create allowed_users.json locally
# 2. Upload bot code
pscp -i "C:\temp\ssh\waywiser\private.ppk" telegram-bot-linux.py root@82.165.141.243:/root/telegram-bot/telegram-bot-linux.py

# 3. Upload whitelist
pscp -i "C:\temp\ssh\waywiser\private.ppk" allowed_users.json root@82.165.141.243:/root/telegram-bot/allowed_users.json

# 4. Restart
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 restart telegram-bot"

# 5. Verify
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 20"
```

---

## Troubleshooting

### "Access control disabled"
- **Cause**: `allowed_users.json` not found
- **Fix**: Upload the file to `/root/telegram-bot/allowed_users.json`

### "Invalid JSON" error
- **Cause**: JSON syntax error
- **Fix**: Validate JSON at https://jsonlint.com/

### User still getting "Access denied"
- **Cause**: User ID not in whitelist
- **Fix**: Double-check user ID from @userinfobot, restart bot

### Need to bypass access control temporarily?
```python
# In handle_update, before the check:
if text == '/bypass-code':
    print("✓ Access check bypassed")
    # Continue without access check
```

---

## Summary

### For Finding User ID:
1. **Fastest**: Use @userinfobot (10 seconds)
2. **Already works**: Send message to your bot and check logs
3. **Programmatic**: Get from message object

### For Managing Whitelist:
1. **Create** `allowed_users.json`
2. **Add user IDs** to the list
3. **Upload** file to server
4. **Restart** bot with PM2

**No password needed** - User IDs are sufficient and secure!

