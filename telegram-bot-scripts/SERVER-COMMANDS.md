# Server Commands - Telegram Bot Management

## SSH Configuration

**SSH Key**: `C:\temp\ssh\waywiser\private.ppk`
**Server**: `82.165.141.243` (mail.y2k.global)
**User**: `root`
**Bot Directory**: `/root/telegram-bot`

## Service Management (PM2)

### Check All Processes
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 list"
```

### Start Bot
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 start telegram-bot"
```

### Stop Bot
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 stop telegram-bot"
```

### Restart Bot
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 restart telegram-bot"
```

### Delete Bot from PM2
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 delete telegram-bot"
```

### Monitor All Processes in Real-Time
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 monit"
```

## Logging (PM2)

### View Recent Logs (Last 20 lines)
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 20"
```

### View Recent Logs (Last 50 lines)
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 50"
```

### Follow Logs in Real-Time
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot"
```

### View Both Stdout and Stderr
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "cat /root/.pm2/logs/telegram-bot-out.log && echo '---' && cat /root/.pm2/logs/telegram-bot-error.log"
```

### Clear Logs
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 flush"
```

## Process Management

### Check Running Processes
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "ps aux | grep telegram-bot | grep -v grep"
```

### Get Process Details
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "ps -p $(pgrep -f telegram-bot) -o pid,cmd,vsz,rss,%cpu,%mem"
```

### Kill Process (Force Stop)
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pkill -f telegram-bot"
```

## File Management

### List Bot Files
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "ls -lah /root/telegram-bot/"
```

### View Bot Script
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "head -20 /root/telegram-bot/telegram-bot-linux.py"
```

### View Configuration
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "cat /root/telegram-bot/.env"
```

### View Service File
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "cat /etc/systemd/system/telegram-bot.service"
```

### Check File Permissions
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "stat /root/telegram-bot/telegram-bot-linux.py"
```

## File Upload/Download

### Upload Bot Script
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" "C:\git\buildyoursite\telegram-bot-scripts\telegram-bot-linux.py" root@82.165.141.243:/root/telegram-bot/telegram-bot-linux.py
```

### Upload Configuration
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" "C:\git\buildyoursite\telegram-bot-scripts\.env" root@82.165.141.243:/root/telegram-bot/.env
```

### Download Bot Script
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243:/root/telegram-bot/telegram-bot-linux.py "C:\local\backup\telegram-bot-linux.py"
```

### Download Configuration
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243:/root/telegram-bot/.env "C:\local\backup\.env"
```

## System Information

### Check Server Resources
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "uname -a && echo '---' && df -h / && echo '---' && free -h"
```

### Check Disk Space
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "du -sh /root/telegram-bot/"
```

### Check Memory Usage
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "free -h"
```

### Check Load Average
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "uptime"
```

## Claude Execution Server

### Check Server Health
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "curl -s http://localhost:5555/health"
```

### Check Server Status with Pretty JSON
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "curl -s http://localhost:5555/health | python3 -m json.tool"
```

### Test Server with Echo
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "curl -s -X POST http://localhost:5555/execute -H 'Content-Type: application/json' -d '{\"prompt\": \"echo test\"}' | python3 -m json.tool"
```

## Troubleshooting Commands

### Full System Diagnostic
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "echo '=== Service Status ===' && systemctl status telegram-bot && echo '=== Recent Logs ===' && journalctl -u telegram-bot -n 10 --no-pager && echo '=== Process Info ===' && ps aux | grep telegram-bot | grep -v grep"
```

### Check All Dependencies
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "echo '=== Python ===' && python3 --version && echo '=== Requests ===' && pip3 show requests && echo '=== Claude Server ===' && curl -s http://localhost:5555/health"
```

### Check Network Connectivity
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "ping -c 1 8.8.8.8 && echo '---' && curl -s -o /dev/null -w 'HTTP Status: %{http_code}\n' https://api.telegram.org/bot/getMe"
```

## Deployment Commands

### Complete Deployment (After File Upload)
```bash
# 1. Make executable
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "chmod +x /root/telegram-bot/telegram-bot-linux.py"

# 2. Reload systemd
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl daemon-reload"

# 3. Restart service
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl restart telegram-bot"

# 4. Check status
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl status telegram-bot"

# 5. View logs
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "journalctl -u telegram-bot -n 20 --no-pager"
```

## Backup Commands

### Backup Bot Files
```bash
mkdir -p C:\local\backup\telegram-bot-$(Get-Date -Format 'yyyyMMdd-HHmmss')
pscp -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243:/root/telegram-bot/* "C:\local\backup\telegram-bot-$(Get-Date -Format 'yyyyMMdd-HHmmss')\\"
```

### Backup Service File
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243:/etc/systemd/system/telegram-bot.service "C:\local\backup\telegram-bot.service.bak"
```

## Useful One-Liners

### Restart and Watch Logs
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl restart telegram-bot && sleep 1 && journalctl -u telegram-bot -f"
```

### Check and Fix Permissions
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "chmod 755 /root/telegram-bot && chmod 644 /root/telegram-bot/* && chmod 755 /root/telegram-bot/telegram-bot-linux.py && ls -la /root/telegram-bot/"
```

### Show Bot Uptime
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl show -p ActiveEnterTimestamp -p ActiveExitTimestamp telegram-bot"
```

## Tips

1. **Use `-f` flag with journalctl** for real-time log watching
2. **Save commands as scripts** for frequent tasks
3. **Always backup** before modifying bot code
4. **Test changes** on local version first
5. **Check Claude Server** health when bot fails to execute commands
6. **Monitor resource usage** if bot becomes slow

---

For more information, see:
- DEPLOYMENT.md - Detailed deployment information
- QUICK-REFERENCE.md - Quick command summary
- README.md - Bot features and usage
