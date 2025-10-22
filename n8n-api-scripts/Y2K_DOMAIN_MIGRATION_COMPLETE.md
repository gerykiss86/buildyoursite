# Y2K.global Domain Migration - COMPLETE

## ✅ Migration Summary

All services have been successfully migrated to use the y2k.global domain:

### n8n Workflow Automation
- **Old URL**: https://n8n.getmybot.pro (now redirects)
- **New URL**: https://n8n.y2k.global
- **Status**: ✅ Fully operational with SSL

### Mail Server Services
- **PostfixAdmin**: https://mailadmin.y2k.global
- **Webmail**: https://webmail.y2k.global (when configured)
- **Mail Server**: mail.y2k.global
- **Status**: ✅ All mail services updated

## What Was Changed

### 1. Server Configuration
- ✅ n8n Docker container updated to use n8n.y2k.global
- ✅ Nginx configuration updated for new domain
- ✅ SSL certificate obtained for n8n.y2k.global
- ✅ Redirect configured from old domain to new

### 2. Local Scripts and Documentation
- ✅ All mailserver documentation updated to use y2k.global
- ✅ All Python scripts updated to use new domains
- ✅ Configuration files (n8n.env) updated
- ✅ CLAUDE.md updated with new URLs

### 3. Removed getmybot.pro References
- 13 mailserver files updated
- 5 n8n scripts updated
- All references replaced with y2k.global equivalents

## Current Access URLs

### n8n
- **URL**: https://n8n.y2k.global
- **API**: https://n8n.y2k.global/api/v1
- **Credentials**:
  - Email: info@kiss-it.io
  - Password: Theworldismine69!

### Mail Server Admin
- **URL**: https://mailadmin.y2k.global
- **Credentials**:
  - Username: admin@y2k.global
  - Password: Admin2025!

## DNS Records Required

Make sure these DNS records are configured:

```
Type    Host        Value               TTL
A       n8n         82.165.141.243      300
A       mail        82.165.141.243      300
A       mailadmin   82.165.141.243      300
A       webmail     82.165.141.243      300
MX      @           mail.y2k.global     300 (Priority: 10)
```

## Testing Commands

### Test n8n API
```bash
python n8n_api_test.py
```

### Test Mail Server
```bash
python mailserver/mailbox_manager.py list
```

### Check Services
```bash
plink -batch -i "C:\temp\ssh\waywiser\private.ppk" root@82.165.141.243 "docker ps | grep n8n"
```

## Backup Information

Configuration backups were created:
- `/opt/n8n/docker-compose.yml.backup-getmybot`
- `/etc/nginx/conf.d/n8n.conf.backup-getmybot`

## Notes

1. The old n8n.getmybot.pro URL automatically redirects to n8n.y2k.global
2. All workflows and data remain intact - only the access URL changed
3. API keys remain the same
4. All login credentials remain unchanged

## Rollback (if needed)

To rollback to the old domain:
```bash
# On server
cp /opt/n8n/docker-compose.yml.backup-getmybot /opt/n8n/docker-compose.yml
cp /etc/nginx/conf.d/n8n.conf.backup-getmybot /etc/nginx/conf.d/n8n.conf
rm /etc/nginx/conf.d/n8n-y2k.conf
rm /etc/nginx/conf.d/n8n-redirect.conf
cd /opt/n8n && docker-compose up -d
systemctl reload nginx
```

---

*Migration completed: 2025-10-22*
*All services operational on y2k.global domain*