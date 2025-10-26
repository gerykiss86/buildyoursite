# Telegram Bot Scripts

Test and automation scripts for the BuildYourSiteProBot Telegram bot.

## Bot Details

- **Bot Name**: BuildYourSiteProBot
- **Bot URL**: https://t.me/BuildYourSiteProBot
- **Bot Token**: `8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4`

⚠️ **Keep your token secure!** Never commit it to version control.

## Available Scripts

### 1. Telegram Bot (Linux Server)

A Telegram bot that integrates with the Claude Execution Server running on the Linux server (port 5555).

**Requirements**:
- Python 3.6+
- requests library
- Claude Execution Server running on port 5555

**Setup**:
```bash
# Install dependencies
pip install requests

# Ensure .env file has the correct CLAUDE_SERVER_URL
# Default: http://localhost:5555

# Run the bot
python3 telegram-bot-linux.py
```

**Features**:
- Echo mode: Repeats any message back
- Claude mode: `claude: your prompt` executes via the execution server
- Automatically handles long responses (splits if > 4096 chars)
- Health check on startup to verify server connectivity
- 5-minute timeout for Claude command execution

### 2. Echo Bot (JavaScript)

A simple bot that echoes back any message it receives.

**Requirements**:
- Node.js 12+

**Setup**:
```bash
# Install dependencies (if any)
npm install

# Set environment variable with your bot token
export BOT_TOKEN="8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4"

# Run the bot
node echo-bot.js
```

**Usage**:
1. Open Telegram and find @BuildYourSiteProBot
2. Send any message
3. The bot will echo it back with "Echo: " prefix

### 2. Echo Bot (Python)

A simple bot that echoes back any message it receives (Python version).

**Requirements**:
- Python 3.6+
- requests library

**Setup**:
```bash
# Install dependencies
pip install requests

# Set environment variable with your bot token
export BOT_TOKEN="8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4"

# Run the bot
python3 echo-bot.py
```

**Usage**:
1. Open Telegram and find @BuildYourSiteProBot
2. Send any message
3. The bot will echo it back with "Echo: " prefix

## How Polling Works

Both scripts use **long polling** to receive updates from Telegram. This means:
- Every second, the bot checks Telegram servers for new messages
- When a message arrives, the bot processes it and sends a response
- The connection stays open for up to 30 seconds waiting for messages (efficiency feature)

## Testing the Bot

### Echo Mode (Default)
Send any message and the bot will echo it back:
- Message: `hello`
- Response: `Echo: hello`

### Claude AI Mode
Send a message starting with `claude:` to execute a Claude AI prompt:

**Syntax**: `claude: your prompt here`

**Examples**:
- `claude: What is 2+2?`
- `claude: Write a Python function to reverse a string`
- `claude: Explain quantum computing in simple terms`

**Features**:
- Executes Claude CLI with `--dangerously-skip-permissions --print` flags
- Automatically splits long responses into multiple messages (Telegram limit is 4096 chars)
- Shows "⏳ Processing..." while the command runs
- Returns full Claude AI output to Telegram
- Error handling with detailed error messages

**Requirements for Claude Mode**:
- Claude Code CLI must be installed and in PATH
- Valid authentication with Claude
- Internet connection

## Environment Variables

Store your bot token and server configuration safely in the `.env` file:

**.env file format**:
```
BOT_TOKEN=8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4
CLAUDE_SERVER_URL=http://localhost:5555
```

**Environment variables (if not using .env)**:

Linux/Mac:
```bash
export BOT_TOKEN="your_token_here"
export CLAUDE_SERVER_URL="http://your-server:5555"
```

Windows (PowerShell):
```powershell
$env:BOT_TOKEN="your_token_here"
$env:CLAUDE_SERVER_URL="http://your-server:5555"
```

Windows (CMD):
```cmd
set BOT_TOKEN=your_token_here
set CLAUDE_SERVER_URL=http://your-server:5555
```

## Telegram Bot API Documentation

For more information about the Telegram Bot API:
- https://core.telegram.org/bots/api
- https://core.telegram.org/bots

## Troubleshooting

### "BOT_TOKEN environment variable not set"
Make sure you've set the environment variable before running the script:
```bash
export BOT_TOKEN="8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4"
```

### "Failed to connect to Telegram"
- Check your internet connection
- Verify the bot token is correct
- Check that the bot is not running on another device/process

### No messages received
- Make sure you're sending messages to @BuildYourSiteProBot
- Check that the bot is running (you should see "Bot started!" message)
- Try sending multiple messages, as there may be a slight delay

### Python: "ModuleNotFoundError: No module named 'requests'"
Install the requests library:
```bash
pip install requests
```

## Choosing the Right Version

| Version | Best For | Requirements | Notes |
|---------|----------|--------------|-------|
| **telegram-bot-linux.py** | Production on Linux server | Python 3.6+, Claude Execution Server running | Recommended for servers, scalable, clean separation |
| **echo-bot.py** | Local development | Python 3.6+, Claude Code CLI installed | Direct execution, simpler setup |
| **echo-bot.js** | Local development | Node.js 12+, Claude Code CLI installed | Alternative local option |

**Recommendation**: Use `telegram-bot-linux.py` on your production Linux server for better security and scalability.

## Future Enhancements

Potential features to add:
- Command handling (e.g., `/start`, `/help`, `/stop`)
- User database to track interactions
- Integration with n8n workflows
- Message logging and analytics
- Admin controls and permissions
- Integration with BuildYourSite website generation
- Email notifications
- Custom keyboard buttons
- Webhook support (alternative to polling)

## Security Notes

1. **Never** commit bot tokens to git
2. **Never** share your bot token publicly
3. Use environment variables for sensitive data
4. Consider using `.env` files (but add to `.gitignore`)
5. Rotate tokens if they are accidentally exposed
