# PM2 Management - Telegram Bot

## Overview

The Telegram Bot is now managed by PM2 (Process Manager 2), the same process manager used for the Claude Execution Server. This ensures:

- ✓ Automatic restarts if the bot crashes
- ✓ Consistent process management across the server
- ✓ Real-time monitoring and logs
- ✓ Auto-start on server reboot
- ✓ Memory and CPU tracking

## PM2 Configuration

**Bot Process Name**: `telegram-bot`
**Script Path**: `/root/telegram-bot/telegram-bot-linux.py`
**Interpreter**: `python3`
**Log Location**: `/root/.pm2/logs/telegram-bot-*`

## PM2 Process List

View all managed processes:

```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 list"
```

**Expected Output**:
```
│ 0  │ profinance-backend    │ running │ 80.4mb   │
│ 2  │ claude-server         │ running │ 32.4mb   │
│ 3  │ telegram-bot          │ running │ 25.3mb   │
```

## Starting and Stopping

### Start the Bot
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 start telegram-bot"
```

### Stop the Bot
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 stop telegram-bot"
```

### Restart the Bot
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 restart telegram-bot"
```

## Viewing Logs

### Real-Time Logs (Follow)
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot"
```

This will stream logs in real-time. Press `Ctrl+C` to exit.

### Last N Lines
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 50"
```

### Out and Error Logs Separately
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "cat /root/.pm2/logs/telegram-bot-out.log"
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "cat /root/.pm2/logs/telegram-bot-error.log"
```

### Clear All Logs
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 flush"
```

## Monitoring

### Real-Time Dashboard
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 monit"
```

This shows CPU and memory usage in real-time for all PM2 processes.

### Detailed Process Information
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 show telegram-bot"
```

**Shows**:
- Process ID (PID)
- Status
- Memory and CPU usage
- Uptime
- Number of restarts
- Last restart time

## Managing Startup

### Save Current Process List
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 save"
```

This saves the current list of PM2 processes to `/root/.pm2/dump.pm2`. These processes will auto-start on server reboot.

### Enable Auto-Start on Boot
The bot is already configured to auto-start on server reboot through PM2 systemd integration.

### Check Auto-Start Status
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "systemctl status pm2-root"
```

## Updating the Bot

### 1. Upload New Bot Script
```bash
pscp -i "C:\temp\ssh\waywiser\private.ppk" telegram-bot-linux.py root@82.165.141.243:/root/telegram-bot/telegram-bot-linux.py
```

### 2. Restart the Bot
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 restart telegram-bot"
```

### 3. Verify Update
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 20"
```

## Troubleshooting

### Bot is Down

**Check Status**:
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 status telegram-bot"
```

**Check Logs for Errors**:
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 30"
```

**Restart**:
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 restart telegram-bot"
```

### High Memory Usage

**Check Memory**:
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 show telegram-bot | grep memory"
```

**Possible Solutions**:
1. Check for memory leaks in logs
2. Restart the bot: `pm2 restart telegram-bot`
3. Check Claude Server connectivity

### Process Keeps Restarting

**Check Restart Count**:
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 show telegram-bot | grep restarts"
```

**View Restart Logs**:
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 logs telegram-bot --lines 50 | tail -30"
```

**Common Causes**:
- Claude Execution Server is down
- Bot token is invalid
- Network connectivity issues

## Comparing PM2 vs Systemd

| Feature | PM2 | Systemd |
|---------|-----|---------|
| Process Management | ✓ Unified | ✓ Individual units |
| Auto-Restart | ✓ Built-in | ✓ Restart policy |
| Real-Time Monitoring | ✓ Dashboard | ✗ Manual checks |
| Logging | ✓ Centralized | ✓ journalctl |
| Multiple Processes | ✓ Excellent | ✓ Multiple files |
| Memory/CPU Tracking | ✓ Built-in | ✗ ps/top needed |
| Auto-Start on Reboot | ✓ Yes | ✓ Yes |

**Why PM2?** Consistency with Claude Server and better monitoring/management capabilities.

## Advanced PM2 Commands

### Watch File Changes (Auto-Restart)
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 watch telegram-bot"
```

### Set Max Memory Limit
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 set telegram-bot max_memory_restart 100M"
```

### View Environment Variables
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "pm2 show telegram-bot | grep env"
```

### Save Logs to External Service
Supported services: AWS, NewRelic, Datadog, etc. (See PM2 documentation)

## PM2 Configuration File (Optional)

For more complex configurations, you can create an ecosystem.config.js file:

```javascript
module.exports = {
  apps: [
    {
      name: 'telegram-bot',
      script: '/root/telegram-bot/telegram-bot-linux.py',
      interpreter: 'python3',
      instances: 1,
      max_memory_restart: '100M',
      error_file: '/root/.pm2/logs/telegram-bot-error.log',
      out_file: '/root/.pm2/logs/telegram-bot-out.log',
      log_file: '/root/.pm2/logs/telegram-bot-combined.log',
      time: true,
      env: {
        'NODE_ENV': 'production'
      }
    }
  ]
};
```

Then start with: `pm2 start ecosystem.config.js`

## PM2 Cluster Mode (Multiple Instances)

Currently the bot runs in single instance mode. To run multiple instances for load balancing:

```bash
pm2 start telegram-bot-linux.py -i max --name telegram-bot
```

Note: This would require load balancing logic on the Telegram polling side.

## Tips and Best Practices

1. **Always save after changes**: `pm2 save`
2. **Monitor regularly**: Use `pm2 monit` for real-time monitoring
3. **Check logs frequently**: Catch issues early with regular log checks
4. **Use descriptive names**: Makes identifying processes easier
5. **Document changes**: Keep track of why processes were restarted
6. **Test updates locally**: Before deploying to production
7. **Keep backup logs**: Archive important logs for troubleshooting

## Related Documentation

- **DEPLOYMENT.md** - Full deployment information
- **QUICK-REFERENCE.md** - Quick command summary
- **SERVER-COMMANDS.md** - Complete server command list
- **README.md** - Bot features and usage

## PM2 Resources

- PM2 Official Docs: https://pm2.keymetrics.io/docs/
- PM2 GitHub: https://github.com/Unitech/pm2
- PM2 API: https://pm2.keymetrics.io/docs/api/

---

**Last Updated**: October 25, 2025
**Deployment Status**: ✓ Running with PM2
