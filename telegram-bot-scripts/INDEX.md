# Telegram Bot Scripts - Documentation Index

## Overview

This directory contains a complete Telegram bot implementation with support for echo messages and Claude AI command execution via a remote execution server.

**Bot**: @BuildYourSiteProBot
**Status**: ✓ Running in Production on 82.165.141.243
**Process Manager**: PM2
**Python Version**: 3.9.19

---

## Documentation Guide

### For Quick Reference (Start Here)
📄 **[QUICK-REFERENCE.md](QUICK-REFERENCE.md)** - _5 min read_
- Essential connection details
- Most common commands
- Quick troubleshooting

### For Comprehensive Information
📄 **[DEPLOYMENT-SUMMARY.md](DEPLOYMENT-SUMMARY.md)** - _10 min read_
- Current deployment status
- All services running
- Performance metrics
- Quick status checks

### For Detailed Deployment Information
📄 **[DEPLOYMENT.md](DEPLOYMENT.md)** - _15 min read_
- Full deployment steps
- Configuration details
- Backup and recovery procedures
- Maintenance checklist

### For Server Command Reference
📄 **[SERVER-COMMANDS.md](SERVER-COMMANDS.md)** - _Complete reference_
- All SSH commands with plink
- File management commands
- Troubleshooting procedures
- Useful one-liners

### For Process Management
📄 **[PM2-MANAGEMENT.md](PM2-MANAGEMENT.md)** - _PM2 specific guide_
- PM2 process management
- Real-time monitoring
- Logging and debugging
- Advanced PM2 features

### For Bot Features and Usage
📄 **[README.md](README.md)** - _Local development guide_
- Bot features explanation
- Local testing instructions
- Python/Node.js versions
- Environment setup

---

## Quick Navigation by Task

### "I need to check if the bot is running"
→ [QUICK-REFERENCE.md](QUICK-REFERENCE.md#common-commands) or
→ [PM2-MANAGEMENT.md](PM2-MANAGEMENT.md#viewing-logs)

### "The bot is not responding"
→ [SERVER-COMMANDS.md](SERVER-COMMANDS.md#troubleshooting-commands) or
→ [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting)

### "I want to update the bot code"
→ [DEPLOYMENT.md](DEPLOYMENT.md#updating-the-bot) or
→ [SERVER-COMMANDS.md](SERVER-COMMANDS.md#deployment-commands)

### "I need to view bot logs"
→ [QUICK-REFERENCE.md](QUICK-REFERENCE.md#view-logs) or
→ [PM2-MANAGEMENT.md](PM2-MANAGEMENT.md#viewing-logs)

### "I want to understand the deployment"
→ [DEPLOYMENT.md](DEPLOYMENT.md) or
→ [DEPLOYMENT-SUMMARY.md](DEPLOYMENT-SUMMARY.md)

### "I need to monitor performance"
→ [PM2-MANAGEMENT.md](PM2-MANAGEMENT.md#monitoring) or
→ [SERVER-COMMANDS.md](SERVER-COMMANDS.md#system-information)

### "I'm testing the bot locally"
→ [README.md](README.md#available-scripts)

### "I need all available commands"
→ [SERVER-COMMANDS.md](SERVER-COMMANDS.md) (Complete reference)

---

## File Structure

```
telegram-bot-scripts/
├── 📋 Documentation
│   ├── INDEX.md                  (This file - Navigation guide)
│   ├── README.md                 (Bot features and local testing)
│   ├── DEPLOYMENT.md             (Full deployment details)
│   ├── DEPLOYMENT-SUMMARY.md     (Current status summary)
│   ├── QUICK-REFERENCE.md        (Quick command reference)
│   ├── SERVER-COMMANDS.md        (Complete command list)
│   └── PM2-MANAGEMENT.md         (PM2 process management)
│
├── 🤖 Bot Scripts (Production - Server)
│   ├── telegram-bot-linux.py     (Main bot for Linux server)
│   └── .env                      (Configuration with bot token)
│
├── 🤖 Bot Scripts (Local Development)
│   ├── echo-bot.py               (Python version - local)
│   └── echo-bot.js               (Node.js version - local)
│
├── 🔧 Utilities
│   ├── deploy-to-server.py       (Deployment automation script)
│   └── setup.sh                  (Linux setup helper)
│
└── 📄 Configuration
    └── .gitignore                (Prevents committing .env)
```

---

## Server Information at a Glance

| Property | Value |
|----------|-------|
| **Host** | 82.165.141.243 |
| **Hostname** | mail.y2k.global |
| **SSH User** | root |
| **SSH Key** | C:\temp\ssh\waywiser\private.ppk |
| **Bot Directory** | /root/telegram-bot |
| **Process Manager** | PM2 |
| **Bot Name** | telegram-bot |
| **Process ID** | 2685261 |
| **Memory** | ~25.5 MB |
| **Status** | ✓ Running |

---

## Most Useful Commands

### Check Bot Status
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 list"
```

### View Bot Logs
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 20"
```

### Restart Bot
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 restart telegram-bot"
```

### Real-Time Monitoring
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 monit"
```

### Update Bot Code
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" telegram-bot-linux.py root@82.165.141.243:/root/telegram-bot/telegram-bot-linux.py
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 restart telegram-bot"
```

---

## Bot Features

### 1. Echo Mode
**Usage**: Send any message
**Response**: Bot echoes the message back

```
You: hello world
Bot: Echo: hello world
```

### 2. Claude AI Mode
**Usage**: Start message with `claude:` prefix
**Response**: Response from Claude Execution Server

```
You: claude: What is the capital of France?
Bot: [Processing...]
Bot: [Claude AI response]
```

---

## Technology Stack

- **Language**: Python 3.9.19
- **Framework**: HTTP requests (no external bot library)
- **Process Manager**: PM2
- **Polling**: Long polling (30s timeout per request)
- **Execution Server**: Flask-based Claude Execution Server
- **SSH Tool**: PuTTY (plink/pscp)

---

## Current Status

✓ **Deployment**: Complete
✓ **Bot**: Running and responding
✓ **Claude Server**: Healthy and executing commands
✓ **Documentation**: Complete and up-to-date
✓ **Auto-Restart**: Enabled via PM2
✓ **Auto-Start on Reboot**: Enabled via PM2 systemd

---

## Getting Started Scenarios

### Scenario 1: "I'm new to this, where do I start?"
1. Read [DEPLOYMENT-SUMMARY.md](DEPLOYMENT-SUMMARY.md)
2. Review [QUICK-REFERENCE.md](QUICK-REFERENCE.md)
3. Use commands from there

### Scenario 2: "Bot is down, fix it NOW!"
1. Run status check from [QUICK-REFERENCE.md](QUICK-REFERENCE.md#check-status)
2. If not running, restart from [QUICK-REFERENCE.md](QUICK-REFERENCE.md#restart-bot)
3. Check logs from [QUICK-REFERENCE.md](QUICK-REFERENCE.md#view-logs)

### Scenario 3: "I need to update the bot code"
1. Check [SERVER-COMMANDS.md](SERVER-COMMANDS.md#deployment-commands)
2. Upload new file via pscp
3. Restart bot with `pm2 restart telegram-bot`

### Scenario 4: "Claude commands are not working"
1. Check Claude Server health from [QUICK-REFERENCE.md](QUICK-REFERENCE.md#check-claude-server)
2. View bot logs from [PM2-MANAGEMENT.md](PM2-MANAGEMENT.md#viewing-logs)
3. Contact Claude Server team if it's down

### Scenario 5: "I want to understand everything"
1. Read [DEPLOYMENT.md](DEPLOYMENT.md) for full context
2. Review [PM2-MANAGEMENT.md](PM2-MANAGEMENT.md) for operations
3. Check [SERVER-COMMANDS.md](SERVER-COMMANDS.md) for reference

---

## Critical Information

⚠️ **Bot Token** (Keep Secure!)
```
8378004706:AAGCDKWgD88ayoBvltTJX03bfigfPgNhiq4
```
Never commit to git or share publicly.

🔐 **SSH Key** (Required for Access)
```
C:\temp\ssh\waywiser\private.ppk
```
Must be kept secure.

---

## Troubleshooting Quick Links

| Problem | Documentation |
|---------|---------------|
| Bot not running | [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting) |
| Claude commands fail | [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting) |
| 409 Conflict Error | [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting) |
| Check resource usage | [SERVER-COMMANDS.md](SERVER-COMMANDS.md#system-information) |
| View real-time logs | [PM2-MANAGEMENT.md](PM2-MANAGEMENT.md#viewing-logs) |
| Restart bot | [QUICK-REFERENCE.md](QUICK-REFERENCE.md#restart-bot) |

---

## Maintenance Schedule

### Daily
- Monitor logs for errors: `pm2 logs telegram-bot`
- Check bot responds to test message

### Weekly
- Review resource usage: `pm2 show telegram-bot`
- Check Claude Server health
- Verify backups are working

### Monthly
- Review deployment documentation
- Update bot code if needed
- Test disaster recovery procedures

---

## Related Systems

### Claude Execution Server
📄 See: ../n8n-api-scripts/CLAUDE.md
- Runs on port 5555
- Managed by PM2
- Executes Claude commands

### n8n Workflow Server
📄 See: ../n8n-api-scripts/CLAUDE.md
- Runs on port 5678 (internal)
- Available at https://n8n.y2k.global
- Workflow automation

---

## Version History

| Date | Version | Status | Notes |
|------|---------|--------|-------|
| Oct 25, 2025 | 1.0 | ✓ Production | Initial deployment with PM2 |

---

## Support and Escalation

1. **For Quick Questions**: Check [QUICK-REFERENCE.md](QUICK-REFERENCE.md)
2. **For Issues**: Check [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting)
3. **For Commands**: Check [SERVER-COMMANDS.md](SERVER-COMMANDS.md)
4. **For PM2 Help**: Check [PM2-MANAGEMENT.md](PM2-MANAGEMENT.md)
5. **For Claude Server Issues**: Check ../n8n-api-scripts/CLAUDE.md

---

## Document Statistics

| Document | Purpose | Read Time | Size |
|----------|---------|-----------|------|
| README.md | Features & local testing | 10 min | 4 KB |
| DEPLOYMENT.md | Full deployment guide | 15 min | 12 KB |
| DEPLOYMENT-SUMMARY.md | Current status | 10 min | 8 KB |
| QUICK-REFERENCE.md | Quick commands | 5 min | 3 KB |
| SERVER-COMMANDS.md | Command reference | 20 min | 15 KB |
| PM2-MANAGEMENT.md | Process management | 15 min | 10 KB |
| INDEX.md | Navigation (this file) | 10 min | 6 KB |

---

## Last Updated

**Date**: October 25, 2025
**Time**: 22:37 UTC
**Status**: ✓ All systems operational

---

**Pro Tip**: Bookmark this INDEX.md file for quick navigation to all documentation!

