# Telegram Bot Deployment Documentation

## Deployment Information

**Date Deployed**: October 25, 2025
**Bot Name**: BuildYourSiteProBot
**Bot Token**: `8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4`
**Bot URL**: https://t.me/BuildYourSiteProBot

## Server Information

| Property | Value |
|----------|-------|
| **Host** | 82.165.141.243 |
| **Hostname** | mail.y2k.global |
| **User** | root |
| **SSH Key** | C:\temp\ssh\waywiser\private.ppk |
| **Bot Directory** | /root/telegram-bot |
| **Service Name** | telegram-bot |

## Deployment Steps Completed

### 1. SSH Connection Test ✓
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "echo 'SSH connection successful' && pwd"
```
**Status**: Connected successfully to /root

### 2. Created Remote Directory ✓
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "mkdir -p /root/telegram-bot"
```
**Status**: Directory created at /root/telegram-bot

### 3. Uploaded Bot Files ✓
- **telegram-bot-linux.py** (7943 bytes) - Main bot script
- **.env** (97 bytes) - Configuration file with bot token

**Upload Tool**: pscp
**Status**: Both files successfully uploaded

### 4. Set Permissions ✓
```bash
chmod +x /root/telegram-bot/telegram-bot-linux.py
```
**Status**: Bot script is executable

### 5. Verified Dependencies ✓
- **Python**: 3.9.19 ✓
- **requests library**: 2.25.1 ✓
- **Claude Execution Server**: Running on http://localhost:5555 ✓

All dependencies are installed and working.

### 6. Created Systemd Service ✓
**Service File**: `/etc/systemd/system/telegram-bot.service`

```ini
[Unit]
Description=BuildYourSite Telegram Bot (Linux)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/telegram-bot
ExecStart=/usr/bin/python3 /root/telegram-bot/telegram-bot-linux.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=telegram-bot
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

**Status**: Service created and enabled

### 7. Started Bot with Systemd Service (Initial) ✓
```bash
systemctl start telegram-bot
systemctl enable telegram-bot
```

**Status**: Service was running and working correctly

### 8. Migrated to PM2 for Better Process Management ✓
Since PM2 was already managing the Claude Execution Server, we switched the bot to PM2 for consistency:

```bash
systemctl stop telegram-bot
systemctl disable telegram-bot
pm2 start telegram-bot-linux.py --name telegram-bot --interpreter python3
pm2 save
pm2 startup
```

**Status**: Bot is now managed by PM2
**Process ID**: 2685261
**Memory Usage**: ~25MB
**CPU Usage**: 0%
**Uptime**: See `pm2 list` for real-time status

## Service Management Commands (Using PM2)

### Check Process Status
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 list"
```

### View Bot Logs (Last 20 lines)
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 20"
```

### Follow Logs in Real-Time
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot"
```

### Restart Bot
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 restart telegram-bot"
```

### Stop Bot
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 stop telegram-bot"
```

### Start Bot
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 start telegram-bot"
```

### Monitor Bot in Real-Time
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 monit"
```

### View Bot Details
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 show telegram-bot"
```

## Initial Log Output

When the service started, it displayed:

```
Oct 25 22:32:48 mail.y2k.global systemd[1]: Started BuildYourSite Telegram Bot (Linux).
Oct 25 22:32:48 mail.y2k.global telegram-bot[2683621]: 🤖 BuildYourSiteProBot (Linux) started!
Oct 25 22:32:48 mail.y2k.global telegram-bot[2683621]: 📡 Polling for updates every second...
Oct 25 22:32:48 mail.y2k.global telegram-bot[2683621]: 🔗 Bot URL: https://t.me/BuildYourSiteProBot
Oct 25 22:32:48 mail.y2k.global telegram-bot[2683621]: 🖥️  Claude Server: http://localhost:5555
Oct 25 22:32:48 mail.y2k.global telegram-bot[2683621]: ✓ Connected as: @BuildYourSiteProBot
Oct 25 22:32:48 mail.y2k.global telegram-bot[2683621]: ✓ Bot ID: 8378004706
Oct 25 22:32:48 mail.y2k.global telegram-bot[2683621]: ✓ Claude Execution Server is running on http://localhost:5555
```

**Status**: Bot successfully connected to Telegram API and Claude Execution Server

## Bot Features

### Echo Mode (Default)
Send any message and the bot echoes it back:
```
You: hello
Bot: Echo: hello
```

### Claude AI Mode
Send messages starting with `claude:` to execute Claude prompts:
```
You: claude: What is 2+2?
Bot: [Processing message...]
Bot: Claude Response:
2 + 2 = 4
```

**How it works**:
1. Bot receives message
2. Forwards prompt to Claude Execution Server (http://localhost:5555)
3. Server executes as `clauderunner` user via Flask API
4. Response is sent back to Telegram
5. Long responses are automatically split (Telegram limit: 4096 chars)

## Configuration

### Environment Variables (.env)
Located at: `/root/telegram-bot/.env`

```
BOT_TOKEN=8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4
CLAUDE_SERVER_URL=http://localhost:5555
```

### To Update Configuration
1. Edit the .env file on your local machine
2. Upload via pscp:
   ```bash
   pscp -i "C:\temp\ssh\waywiser\private.ppk" .env root@82.165.141.243:/root/telegram-bot/.env
   ```
3. Restart the service:
   ```bash
   plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl restart telegram-bot"
   ```

## File Locations

| File | Location | Purpose |
|------|----------|---------|
| Bot Script | `/root/telegram-bot/telegram-bot-linux.py` | Main Python bot code |
| Configuration | `/root/telegram-bot/.env` | Bot token and server URL |
| Service File | `/etc/systemd/system/telegram-bot.service` | Systemd service definition |
| Logs | journalctl (systemd logs) | Real-time application logs |

## Troubleshooting

### Bot is not responding to messages

**Step 1**: Check service is running
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl is-active telegram-bot"
```

**Step 2**: View recent logs
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "journalctl -u telegram-bot -n 30 --no-pager"
```

**Step 3**: Restart service
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl restart telegram-bot"
```

### Claude commands are failing

**Step 1**: Check Claude Execution Server is running
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "curl -s http://localhost:5555/health"
```

**Expected output**:
```json
{"service":"claude-execution-server","status":"healthy"}
```

**Step 2**: If server is not running, start it (consult Claude Execution Server documentation)

### 409 Conflict Error

This error indicates multiple bot instances are polling Telegram simultaneously. This is normal during restarts and will resolve automatically as old connections timeout (typically within a few minutes).

If the error persists:
1. Restart the service: `systemctl restart telegram-bot`
2. Wait 30 seconds for Telegram to recognize the new connection
3. Check logs: `journalctl -u telegram-bot -f`

## Performance Monitoring

### Check Resource Usage
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "ps aux | grep telegram-bot | grep -v grep"
```

### Check Disk Space
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "df -h /root"
```

### View System Memory
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "free -h"
```

## Backup and Recovery

### Backup Configuration
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243:/root/telegram-bot/.env backup-.env.bak
```

### Restore Configuration
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" backup-.env.bak root@82.165.141.243:/root/telegram-bot/.env
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl restart telegram-bot"
```

## Updating the Bot

### Deploy New Version
1. Update bot script locally
2. Upload new version:
   ```bash
   pscp -i "C:\temp\ssh\waywiser\private.ppk" telegram-bot-linux.py root@82.165.141.243:/root/telegram-bot/telegram-bot-linux.py
   ```
3. Restart service:
   ```bash
   plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl restart telegram-bot"
   ```
4. Verify with logs:
   ```bash
   plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "journalctl -u telegram-bot -n 10"
   ```

## Testing the Bot

### Local Testing
1. Open Telegram and search for @BuildYourSiteProBot
2. Send: `hello`
3. Expect response: `Echo: hello`
4. Send: `claude: What is the capital of France?`
5. Expect: Claude response from execution server

### Automated Testing
You can create a test script to send messages via Telegram API:
```python
import requests

BOT_TOKEN = "8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4"
CHAT_ID = "YOUR_CHAT_ID"  # Get from @userinfobot

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": "claude: Test message"
})
```

## Related Documentation

- **Bot Code**: See README.md for feature documentation
- **n8n Integration**: See ../n8n-api-scripts/CLAUDE.md
- **Server Management**: SSH access via plink commands documented above

## Maintenance Checklist

- [ ] Service is running: `systemctl status telegram-bot`
- [ ] Claude Execution Server is healthy: `curl http://localhost:5555/health`
- [ ] Bot responds to echo messages
- [ ] Bot executes Claude commands
- [ ] Disk space is adequate: `df -h`
- [ ] Service memory usage is normal: `ps aux | grep telegram-bot`
- [ ] Recent logs show no errors: `journalctl -u telegram-bot -n 20`

## Support

For issues or questions:
1. Check logs: `journalctl -u telegram-bot -f`
2. Verify Claude Execution Server is running
3. Check network connectivity to Telegram API
4. Review DEPLOYMENT.md (this file) for common solutions
5. Contact: Check ../n8n-api-scripts/CLAUDE.md for server access info

---

**Last Updated**: October 25, 2025
**Deployment Status**: ✓ Active and Running
