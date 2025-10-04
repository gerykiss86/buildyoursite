# Claude Execution Server - Secure Access Guide

## Server Configuration
- **Server**: 82.165.141.243
- **Port**: 5555 (localhost only)
- **Status**: Running with PM2, auto-starts on boot
- **Security**: Only accessible from localhost (127.0.0.1)

## Access Methods

### 1. From n8n Docker Container

Since the server only listens on localhost, n8n needs to access it through the host network.

#### Option A: Use host networking mode
If n8n container is running with `--network host`:
```json
{
  "method": "POST",
  "url": "http://127.0.0.1:5555/execute",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "prompt": "Your command here"
  }
}
```

#### Option B: Use host.docker.internal (Docker Desktop)
If using Docker Desktop:
```json
{
  "method": "POST",
  "url": "http://host.docker.internal:5555/execute",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "prompt": "Your command here"
  }
}
```

#### Option C: SSH Tunnel from n8n
Use SSH command in n8n to execute through tunnel:
```bash
ssh root@localhost 'curl -X POST http://127.0.0.1:5555/execute -H "Content-Type: application/json" -d "{\"prompt\": \"{{ $json.prompt }}\"}"'
```

### 2. Direct Server Access (for testing)

SSH into the server and use curl:
```bash
# Test health
curl http://127.0.0.1:5555/health

# Execute command
curl -X POST http://127.0.0.1:5555/execute \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your command here"}'
```

## Example Prompts

### Simple Test
```json
{
  "prompt": "Print only: Hello from Claude"
}
```

### Website Deployment
```json
{
  "prompt": "1. Unzip the zip file located in: /path/to/file.zip 2. Change into the extracted project folder. 3. Build the project using npm run build. 4. Deploy the build output to a new subfolder under: /var/www/skykey/ (subfolder name = company-demo). 5. Print ONLY the complete deployment URL in the format https://company-demo.skykey.at"
}
```

### File Operations
```json
{
  "prompt": "1. Change to /opt directory. 2. Create a test.txt file. 3. Write 'Test content' to the file. 4. Print only: Task completed"
}
```

## Server Management

### Check Status
```bash
pm2 status
pm2 logs claude-server
```

### Restart Server
```bash
pm2 restart claude-server
```

### Stop Server
```bash
pm2 stop claude-server
```

### Start Server
```bash
pm2 start claude-server
```

## Security Notes

✅ **Secure Configuration:**
- Server only listens on 127.0.0.1 (localhost)
- Port 5555 is NOT open in firewall
- External access is completely blocked
- Only accessible from the server itself or through proper Docker networking

⚠️ **Important:**
- Never expose port 5555 to the internet
- Always use localhost/127.0.0.1 for access
- For Docker containers, ensure proper network configuration
- Claude runs with `--dangerously-skip-permissions` so handle with care

## Troubleshooting

### If n8n can't connect:
1. Check if n8n container can reach host:
   ```bash
   docker exec <n8n-container> ping host.docker.internal
   ```

2. Check server is running:
   ```bash
   pm2 status
   ```

3. Test locally on server:
   ```bash
   curl http://127.0.0.1:5555/health
   ```

### Common Issues:
- **Connection refused**: Server not running or wrong URL
- **Timeout**: Using external IP instead of localhost
- **No response**: Check PM2 logs for errors