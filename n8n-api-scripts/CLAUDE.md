# n8n Environment Documentation

## Overview
This documentation provides comprehensive instructions for interacting with the n8n workflow automation platform deployed on a Linux server via Docker.

## Environment Architecture

```
┌─────────────────────────────────────────┐
│         n8n.getmybot.pro                 │
│         (HTTPS Frontend)                 │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│     Linux Server (82.165.141.243)       │
│  ┌────────────────────────────────────┐ │
│  │   n8n Docker Container              │ │
│  │   - Port: 127.0.0.1:5678           │ │
│  │   - Volume: /opt/n8n               │ │
│  │   - Data: /home/node/.n8n          │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Credentials and Configuration

### n8n Web Interface
- **URL**: https://n8n.getmybot.pro
- **Email**: info@kiss-it.io
- **Password**: Theworldismine69!

### n8n API Access
- **API Endpoint**: https://n8n.getmybot.pro/api/v1
- **API Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5MGFkODUwMS1iZTBlLTRhM2QtYTA3Mi02YjgwYjliMzU3NWEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU5NTc0ODExfQ.5mf1ZS6bd92j4W3Wv4xXKhxtQVHKL6yM_vke676c6kY`

### SSH Server Access
- **Host**: 82.165.141.243
- **User**: root
- **SSH Key**: C:\temp\ssh\waywiser\private.ppk

### SMTP Configuration (Email)
- **Host**: smtp.easyname.com
- **Port**: 587
- **Username**: 60164mail14
- **Password**: Theworldismine69
- **From Address**: admin@kiss-it.io
- **Security**: STARTTLS

### Docker Configuration
- **Container Name**: n8n
- **Image**: n8nio/n8n:latest
- **Installation Path**: /opt/n8n
- **Data Volume**: n8n_data

## Available Scripts and Tools

### 1. n8n API Test Script (`n8n_api_test.py`)
Quick script to test API connectivity and list workflows.

```bash
python n8n_api_test.py
```

### 2. n8n Workflow Manager (`n8n_workflow_manager.py`)
Interactive CLI tool for managing workflows via API.

```bash
python n8n_workflow_manager.py
```

Features:
- List all workflows
- Get workflow details
- Activate/deactivate workflows
- Execute workflows manually
- View execution history
- Manage credentials

### 3. n8n Docker Manager (`n8n_ssh_commands.py`)
SSH-based Docker container management tool.

```bash
python n8n_ssh_commands.py
```

Features:
- Check container status
- View container logs
- Restart/stop/start container
- Backup n8n data
- Update n8n to latest version
- Check disk usage

### 4. Email Tester (`test_email.py`)
Test and validate SMTP configuration.

```bash
python test_email.py
```

Features:
- Test SMTP connection
- Send test emails
- Send custom emails

### 5. Quick Email Test (`quick_email_test.py`)
Simple script for quick SMTP validation.

```bash
python quick_email_test.py
```

## Common Commands

### SSH Commands (via plink)

Check n8n container status:
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "docker ps | grep n8n"
```

View n8n logs:
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "docker logs --tail 50 n8n"
```

Restart n8n container:
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "docker restart n8n"
```

Access n8n shell:
```bash
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "docker exec -it n8n /bin/sh"
```

### API Commands (using curl or Python)

List all workflows:
```bash
curl -H "X-N8N-API-KEY: YOUR_API_KEY" https://n8n.getmybot.pro/api/v1/workflows
```

Execute a workflow:
```bash
curl -X POST -H "X-N8N-API-KEY: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  https://n8n.getmybot.pro/api/v1/workflows/WORKFLOW_ID/execute
```

## Current Workflows

### buildyoursite (ID: UP0MowU4xpBOOE9J)
**Status**: Active
**Purpose**: Automated site building and deployment workflow

**Nodes**:
1. Email Trigger (IMAP) - Monitors incoming emails
2. Generate Site with Bolt - Creates website using Bolt
3. Parse output folder - Processes generated files
4. Deploy site with Claude - Deploys to production
5. Extract website URL - Gets deployment URL
6. Send email to office - Notification email
7. SMS notifications - Sends SMS to Rami and Gery
8. Cleanup processes - Cleans up bolt-playwright and claude processes

## Troubleshooting

### Common Issues and Solutions

#### 1. API Connection Failed
- Verify API key is correct
- Check if n8n container is running
- Ensure HTTPS certificate is valid

#### 2. SSH Connection Issues
- Verify SSH key path is correct
- Check server firewall rules
- Ensure SSH service is running

#### 3. SMTP Email Failures
- Verify SMTP credentials
- Check firewall allows port 587
- Ensure STARTTLS is enabled

#### 4. Container Not Starting
```bash
# Check docker logs
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "docker logs n8n"

# Check docker-compose configuration
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "cat /opt/n8n/docker-compose.yml"

# Restart container
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "cd /opt/n8n && docker-compose restart"
```

#### 5. Workflow Execution Errors
- Check workflow node configurations
- Review execution logs in n8n UI
- Verify all credentials are active

## Security Considerations

1. **API Key Storage**: Store API keys in environment variables, never hardcode
2. **SSH Key Protection**: Keep private SSH key secure and use passphrase
3. **SMTP Credentials**: Use app-specific passwords when available
4. **Docker Security**: Run container with minimal privileges
5. **Network Security**: Use HTTPS for all API communications

## Backup and Recovery

### Manual Backup
```bash
# Create backup via SSH
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 \
  "docker exec n8n tar -czf /tmp/n8n_backup.tar.gz /home/node/.n8n && \
   docker cp n8n:/tmp/n8n_backup.tar.gz /root/n8n_backup_$(date +%Y%m%d).tar.gz"
```

### Restore from Backup
```bash
# Stop container
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "docker stop n8n"

# Restore data
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 \
  "docker cp /root/n8n_backup.tar.gz n8n:/tmp/ && \
   docker exec n8n tar -xzf /tmp/n8n_backup.tar.gz -C /"

# Start container
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "docker start n8n"
```

## Performance Monitoring

### Check Resource Usage
```bash
# Container stats
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "docker stats n8n --no-stream"

# Disk usage
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "df -h /"

# Memory usage
plink -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "free -h"
```

## Development Workflow

### 1. Test Changes Locally
- Use the Python scripts to test API connectivity
- Validate SMTP configuration
- Check SSH access

### 2. Deploy to Production
- Backup existing data
- Update configuration files
- Restart container
- Verify functionality

### 3. Monitor
- Check container logs
- Review execution history
- Monitor resource usage

## Quick Reference

| Component | Value |
|-----------|-------|
| n8n URL | https://n8n.getmybot.pro |
| API Base | https://n8n.getmybot.pro/api/v1 |
| SSH Host | 82.165.141.243 |
| Docker Path | /opt/n8n |
| Container | n8n |
| SMTP Server | smtp.easyname.com:587 |

## Support and Resources

- **n8n Documentation**: https://docs.n8n.io/
- **n8n Community**: https://community.n8n.io/
- **Docker Documentation**: https://docs.docker.com/
- **API Reference**: https://docs.n8n.io/api/

## Notes

- The n8n instance is configured to run on localhost (127.0.0.1:5678) and is accessible via reverse proxy at https://n8n.getmybot.pro
- Email triggers use IMAP to monitor incoming emails
- Workflow executions can be triggered via API, webhooks, or email
- The system includes automated cleanup processes for bolt-playwright and claude
- All timestamps are in UTC unless otherwise specified

---

*Last Updated: 2025-10-04*
*Environment Version: n8n:latest (Docker)*