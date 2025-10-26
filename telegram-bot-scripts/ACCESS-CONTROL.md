# Telegram Bot Access Control

Yes! You can restrict who can chat with your bot in several ways:

## Option 1: Whitelist Specific User IDs (Recommended)

This is the most straightforward approach. Only users with specific Telegram IDs can use the bot.

### Implementation

Add this function to the bot:

```python
# Allowed users configuration
ALLOWED_USERS = [
    5092208953,      # Gergo
    123456789,       # Other user
    987654321,       # Another user
]

def is_user_allowed(user_id):
    """Check if user is in whitelist"""
    return user_id in ALLOWED_USERS

def handle_update(update):
    """Process incoming updates"""
    if 'message' not in update:
        return

    message = update['message']
    chat_id = message['chat']['id']
    user_id = message['from']['id']
    user_name = message['from'].get('first_name', 'Unknown')
    text = message.get('text', '')

    # NEW: Check if user is allowed
    if not is_user_allowed(user_id):
        send_message(chat_id, '❌ Access denied. You are not authorized to use this bot.')
        print(f"⛔ Unauthorized access attempt by {user_name} (ID: {user_id})")
        return

    # Rest of the code...
```

### Pros:
✓ Simple and straightforward
✓ Fast (no database needed)
✓ Easy to manage small lists
✓ No external dependencies

### Cons:
✗ Need to hardcode user IDs
✗ Requires code changes to add/remove users
✗ Not scalable for large user bases

---

## Option 2: Whitelist with Configuration File

Store allowed users in the `.env` file or a separate JSON file.

### Using .env File

Update `.env`:
```
BOT_TOKEN=8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4
CLAUDE_SERVER_URL=http://localhost:5555
ALLOWED_USERS=5092208953,123456789,987654321
```

Implementation:
```python
def load_allowed_users():
    """Load allowed users from .env"""
    allowed_str = env_vars.get('ALLOWED_USERS', '')
    if not allowed_str:
        return []
    return [int(uid.strip()) for uid in allowed_str.split(',')]

ALLOWED_USERS = load_allowed_users()
```

### Using JSON File

Create `allowed_users.json`:
```json
{
  "allowed_users": [
    {
      "id": 5092208953,
      "name": "Gergo",
      "role": "admin"
    },
    {
      "id": 123456789,
      "name": "User2",
      "role": "user"
    }
  ]
}
```

Implementation:
```python
import json

def load_allowed_users():
    """Load allowed users from JSON"""
    try:
        with open('allowed_users.json', 'r') as f:
            data = json.load(f)
        return {u['id']: u for u in data['allowed_users']}
    except FileNotFoundError:
        return {}

ALLOWED_USERS = load_allowed_users()

def is_user_allowed(user_id):
    return user_id in ALLOWED_USERS

def get_user_role(user_id):
    return ALLOWED_USERS.get(user_id, {}).get('role', 'user')
```

### Pros:
✓ Configuration-driven (no code changes)
✓ Can include metadata (roles, names)
✓ Easier to manage
✓ Can hot-reload

### Cons:
✗ Need to upload file to server
✗ Slightly more complex

---

## Option 3: Whitelist with Chat IDs (Group Access)

Allow specific chat rooms/groups, not just individual users.

```python
ALLOWED_CHATS = [
    5092208953,      # Gergo's private chat
    -1001234567890,  # Group ID (negative number)
]

def is_chat_allowed(chat_id):
    """Check if chat is authorized"""
    return chat_id in ALLOWED_CHATS

def handle_update(update):
    """Process incoming updates"""
    if 'message' not in update:
        return

    message = update['message']
    chat_id = message['chat']['id']

    # Check if chat is allowed
    if not is_chat_allowed(chat_id):
        send_message(chat_id, '❌ This bot is not authorized for this chat.')
        return

    # Rest of code...
```

### Pros:
✓ Control access per group/chat
✓ One bot, multiple authorized chats
✓ Easy to add/remove chats

### Cons:
✗ Need to know group IDs
✗ Different IDs for different groups

---

## Option 4: Role-Based Access Control

Different permissions for different users.

```python
ALLOWED_USERS = {
    5092208953: {
        "name": "Gergo",
        "role": "admin",
        "permissions": ["echo", "claude"]
    },
    123456789: {
        "name": "User2",
        "role": "user",
        "permissions": ["echo"]  # Can only echo, not execute Claude
    }
}

def is_user_allowed(user_id):
    return user_id in ALLOWED_USERS

def has_permission(user_id, permission):
    if user_id not in ALLOWED_USERS:
        return False
    return permission in ALLOWED_USERS[user_id].get('permissions', [])

def handle_update(update):
    """Process incoming updates"""
    # ... existing code ...

    # Check if user is allowed
    if not is_user_allowed(user_id):
        send_message(chat_id, '❌ Access denied.')
        return

    # Claude commands - only for users with 'claude' permission
    if text.lower().startswith('claude:'):
        if not has_permission(user_id, 'claude'):
            send_message(chat_id, '❌ You do not have permission to execute Claude commands.')
            return
        # Execute Claude...
```

### Pros:
✓ Fine-grained control
✓ Different features for different users
✓ Audit trail possible
✓ Flexible

### Cons:
✗ More complex code
✗ More maintenance

---

## Option 5: Admin Command to Manage Users

Allow admins to add/remove users without redeploying.

```python
ADMIN_USERS = [5092208953]  # Only Gergo can manage users
ALLOWED_USERS = set()  # Start empty

def handle_update(update):
    """Process incoming updates"""
    # ... existing code ...

    user_id = message['from']['id']
    text = message.get('text', '')

    # Admin commands
    if text.startswith('/admin'):
        if user_id not in ADMIN_USERS:
            send_message(chat_id, '❌ Admin only command.')
            return

        if text.startswith('/admin add'):
            try:
                new_user_id = int(text.split()[2])
                ALLOWED_USERS.add(new_user_id)
                send_message(chat_id, f'✓ User {new_user_id} added.')
            except:
                send_message(chat_id, '❌ Usage: /admin add <user_id>')

        elif text.startswith('/admin remove'):
            try:
                user_to_remove = int(text.split()[2])
                ALLOWED_USERS.discard(user_to_remove)
                send_message(chat_id, f'✓ User {user_to_remove} removed.')
            except:
                send_message(chat_id, '❌ Usage: /admin remove <user_id>')

        elif text.startswith('/admin list'):
            send_message(chat_id, f'Allowed users: {ALLOWED_USERS}')

        return

    # Regular user access check
    if not is_user_allowed(user_id):
        send_message(chat_id, '❌ Access denied.')
        return

    # ... rest of code ...
```

### Pros:
✓ Dynamic user management
✓ No code redeploy needed
✓ Real-time updates

### Cons:
✗ Need database for persistence
✗ More complex
✗ Users lost after restart (unless saved to file)

---

## How to Find Your User ID

If you don't know your Telegram user ID, use this bot:
- Search for `@userinfobot` on Telegram
- Send it any message
- It will respond with your User ID

For groups:
- Add `@userinfobot` to a group
- Send a message
- It shows the group ID (negative number)

---

## Recommended Implementation

For your use case, I recommend **Option 2 (Configuration File)** because:

1. ✓ Simple to implement
2. ✓ No code changes needed to add users
3. ✓ Can be version controlled (with dummy values)
4. ✓ Easy to manage on the server
5. ✓ Scalable for up to hundreds of users

### Quick Implementation Steps

1. **Create `allowed_users.json` on the server:**
```json
{
  "allowed_users": [
    {"id": 5092208953, "name": "Gergo"}
  ]
}
```

2. **Update bot code** with access control function

3. **Upload to server:**
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" allowed_users.json root@82.165.141.243:/root/telegram-bot/allowed_users.json
```

4. **Restart bot:**
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 restart telegram-bot"
```

---

## Access Control Comparison Table

| Method | Complexity | Flexibility | Management | Scalability |
|--------|-----------|------------|-----------|------------|
| Hardcoded IDs | ⭐ | ⭐ | Code changes | Poor |
| .env Config | ⭐⭐ | ⭐⭐ | Edit .env | Good |
| JSON File | ⭐⭐ | ⭐⭐⭐ | Upload file | Good |
| Chat IDs | ⭐ | ⭐⭐ | Code changes | Good |
| Role-Based | ⭐⭐⭐ | ⭐⭐⭐⭐ | Config file | Excellent |
| Admin Commands | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Runtime | Excellent |

---

## Security Notes

1. **Don't hardcode IDs in public repositories**
2. **Use .gitignore for allowed_users.json**
3. **Log unauthorized access attempts**
4. **Consider rate limiting**
5. **For critical operations, use admin passwords too**

---

## Want Implementation?

Let me know which option you prefer, and I'll:

1. Update the bot code with access control
2. Create the configuration file
3. Update documentation
4. Deploy to the server
5. Test it works

**Which option do you prefer?**
- Option 1: Hardcoded whitelist
- Option 2: .env configuration
- Option 3: JSON file (recommended)
- Option 4: Role-based access
- Option 5: Admin commands

Or just let me know your specific requirement!

