# Telegram Bot - Quick Reference

## Connection Details

```
Server: 82.165.141.243 (mail.y2k.global)
User: root
SSH Key: C:\temp\ssh\waywiser\private.ppk
Bot Directory: /root/telegram-bot
Service: telegram-bot
Bot Token: 8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4
```

## Common Commands (PM2)

### Check Status (All Processes)
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 list"
```

### View Bot Logs
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 20"
```

### Real-Time Logs
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

### Monitor Real-Time
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 monit"
```

## Upload New Bot Version
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" telegram-bot-linux.py root@82.165.141.243:/root/telegram-bot/telegram-bot-linux.py
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl restart telegram-bot"
```

## Upload New Configuration
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" .env root@82.165.141.243:/root/telegram-bot/.env
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl restart telegram-bot"
```

## Check Claude Server
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "curl -s http://localhost:5555/health"
```

## Expected Response
```json
{"service":"claude-execution-server","status":"healthy"}
```

## Bot Usage

### Echo Message
Send to @BuildYourSiteProBot: `hello`
Response: `Echo: hello`

### Claude Command
Send to @BuildYourSiteProBot: `claude: What is 2+2?`
Response: Gets response from Claude Execution Server

## Files on Server

```
/root/telegram-bot/
├── telegram-bot-linux.py    (Main bot script)
├── .env                     (Configuration)
└── [no other files needed]

/etc/systemd/system/
└── telegram-bot.service     (Service definition)
```

## Files on Local Machine

```
C:\git\buildyoursite\telegram-bot-scripts\
├── telegram-bot-linux.py    (Source code)
├── echo-bot.py              (Alternative local version)
├── echo-bot.js              (Alternative local version)
├── .env                     (Configuration)
├── README.md                (Feature documentation)
├── DEPLOYMENT.md            (Detailed deployment guide)
├── QUICK-REFERENCE.md       (This file)
└── deploy-to-server.py      (Deployment script - not used)
```

## SSH Key Info
- Path: `C:\temp\ssh\waywiser\private.ppk`
- Format: PuTTY Private Key
- Used for: plink and pscp commands

## Troubleshooting Quick Guide

| Issue | Command | Solution |
|-------|---------|----------|
| Bot not running | `systemctl status telegram-bot` | `systemctl start telegram-bot` |
| Check logs | `journalctl -u telegram-bot -n 30` | Review error messages |
| Claude server down | `curl http://localhost:5555/health` | Restart Claude server |
| Restart bot | | `systemctl restart telegram-bot` |
| Update bot code | Upload new file | `systemctl restart telegram-bot` |

## Service Auto-Restart

The bot service is configured to:
- Auto-restart if it crashes
- Restart delay: 10 seconds
- Auto-start on server reboot
- Run as root user

## Logs Location

Logs are stored in systemd journal. Access with:
```bash
journalctl -u telegram-bot [OPTIONS]
```

**Useful options**:
- `-f` = Follow (real-time)
- `-n 20` = Last 20 lines
- `--since "2 hours ago"` = Since specific time
- `--no-pager` = Don't paginate

## Performance Baseline

Initial deployment (Oct 25, 2025):
- Memory: ~25MB
- CPU: 0.7%
- Process ID: 2683621
- Status: ✓ Running

---

For detailed information, see DEPLOYMENT.md
