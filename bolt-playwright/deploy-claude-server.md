# Claude Execution Server Deployment Instructions

## 1. Install Dependencies on Server

```bash
# Install Python and pip
yum install -y python3 python3-pip

# Install Flask and dependencies
pip3 install flask flask-cors
```

## 2. Deploy the Server

```bash
# Create directory for the server
mkdir -p /opt/claude-server
mkdir -p /var/log/claude-server

# Copy the server script
cp claude-execution-server.py /opt/claude-server/

# Make it executable
chmod +x /opt/claude-server/claude-execution-server.py
```

## 3. Install as a Service (Optional)

```bash
# Copy service file
cp claude-server.service /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable and start the service
systemctl enable claude-server
systemctl start claude-server

# Check status
systemctl status claude-server
```

## 4. Or Run Directly for Testing

```bash
# Run in background
cd /opt/claude-server
nohup python3 claude-execution-server.py > /var/log/claude-server/output.log 2>&1 &

# Or run in foreground for testing
python3 /opt/claude-server/claude-execution-server.py
```

## 5. Configure Firewall (if needed)

```bash
# Open port 5555
firewall-cmd --permanent --add-port=5555/tcp
firewall-cmd --reload
```

## 6. Test the Server

```bash
# From the server itself
curl http://localhost:5555/health

# Test simple execution
curl -X POST http://localhost:5555/execute \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Output only: Hello from Claude Server"}'

# Test deployment prompt
curl -X POST http://localhost:5555/execute \
  -H "Content-Type: application/json" \
  -d '{"prompt": "1. Unzip /path/to/file.zip 2. Build project 3. Deploy to /var/www/skykey/test-demo 4. Output URL: https://test-demo.skykey.at"}'
```

## 7. Access from Docker Container (n8n)

In your n8n workflow, use HTTP Request node:

### For Simple Test:
- **Method**: POST
- **URL**: `http://host.docker.internal:5555/execute` (or use actual server IP)
- **Body Type**: JSON
- **Body**:
```json
{
  "prompt": "Output only: Hello from n8n"
}
```

### For Deployment:
- **Method**: POST
- **URL**: `http://host.docker.internal:5555/execute`
- **Body Type**: JSON
- **Body**:
```json
{
  "prompt": "1. Unzip the zip file located in: {{ $json.stdout }} 2. Change into the extracted project folder. 3. Build the project. 4. Deploy the build output to a new subfolder under: /var/www/skykey/ (subfolder name = short company name + demo). 5. Print ONLY the complete deployment URL in the format https://<subfolder>.skykey.at"
}
```

## 8. Monitor Logs

```bash
# If running as service
journalctl -u claude-server -f

# If running with nohup
tail -f /var/log/claude-server/output.log
```

## 9. Test with Python Script

```bash
# Copy test script to server or Docker container
python3 test-claude-server.py localhost

# Or from Docker
python3 test-claude-server.py <server-ip>
```

## Troubleshooting

1. **Port already in use**: Change port in environment variable `CLAUDE_SERVER_PORT`
2. **Permission denied**: Ensure the server runs as root or has sudo permissions for `su`
3. **Claude not found**: Ensure claude is installed and available in clauderunner's PATH
4. **Connection refused from Docker**: Use actual server IP instead of localhost/127.0.0.1

## Security Notes

- The server runs commands as `clauderunner` user
- Consider adding authentication if exposed to network
- Use HTTPS in production with proper certificates
- Restrict access to port 5555 to trusted sources only