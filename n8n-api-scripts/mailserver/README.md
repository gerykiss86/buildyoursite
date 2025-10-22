# Mailcow Installation & Configuration Guide

Complete documentation for Mailcow mail server setup, configuration, troubleshooting, branding, and email authentication.

## Table of Contents
1. [Installation Overview](#installation-overview)
2. [Access Information](#access-information)
3. [Current Issues & Fixes](#current-issues--fixes)
4. [DNS Records Configuration](#dns-records-configuration)
5. [Email Authentication & IPv6 PTR Setup](#email-authentication--ipv6-ptr-setup)
6. [Branding & Customization](#branding--customization)
7. [Management & Troubleshooting](#management--troubleshooting)

---

## Installation Overview

Mailcow has been successfully installed and is running on the server with all Docker containers operational.

### Quick Facts
- **Installation Path**: `/opt/mailcow-dockerized`
- **Domain**: `y2k.global`
- **Mail Server URL**: `https://mail.y2k.global`
- **Admin URL**: `https://mail.y2k.global/admin`
- **Webmail URL**: `https://webmail.y2k.global` (redirects to `/SOGo/`)
- **Internal HTTP Port**: 8090
- **Internal HTTPS Port**: 8453
- **Proxy**: Nginx reverse proxy (external 443 → internal 8453)

---

## Access Information

### Web Interface Login
- **Admin Panel**: https://mail.y2k.global/admin/
- **Username**: admin
- **Password**: Admin2025!
- **Webmail (SOGo)**: https://webmail.y2k.global/

### Key Configuration Details
- **Installation Path**: `/opt/mailcow-dockerized`
- **Data Volume**: `n8n_data` (Docker volume)
- **Database**: MySQL running in Docker
- **Cache**: Redis running in Docker
- **Email Scanning**: Rspamd, ClamAV
- **Webmail**: SOGo Groupware

---

## Current Issues & Fixes

### 1. Admin Panel Rendering Issue (FIXED ✓)

**Problem**: Admin panel was loading without CSS/JavaScript (404 errors on static assets)

**Root Cause**: Nginx location blocks were too specific and didn't match paths like `/cache/`, `/css/`, `/js/`

**Solution Applied**: Added catch-all `location /` block in nginx configuration

**File Modified**: `/etc/nginx/conf.d/mailcow.conf`

```nginx
# Default catch-all for everything else (admin, api, static files, etc.)
location / {
    proxy_pass https://127.0.0.1:8453;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Port $server_port;

    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    proxy_connect_timeout 600;
    proxy_send_timeout 600;
    proxy_read_timeout 600;
    send_timeout 600;
}
```

**Verification**: All static assets now load successfully (CSS, JS, fonts return HTTP 200 OK)

---

### 2. Mailbox Management Page Issue (FIXED ✓)

**Problem**: Mailbox management page loading infinitely with JavaScript errors

**Errors**:
- Duplicate element IDs: `#addMailbox_tags`, `#dkim_selector`, `#key_size`
- JavaScript error: `Cannot read properties of null (reading 'imap_access')`
- Malformed mailbox with NULL username in database

**Root Cause**: API returning mailbox data without `attributes` object; null username mailbox in database

**Solutions Applied**:

1. **Added defensive null checks in JavaScript** (file: `/opt/mailcow-dockerized/data/web/js/site/mailbox.js`)
   - Line 907: Added fallback for missing `item.attributes`
   - Line 925: Added null checks before accessing `item.attributes.passwd_update`

2. **Deleted malformed database record**:
   ```sql
   DELETE FROM mailbox WHERE username IS NULL OR username = "" OR username = "null";
   ```

**Verification**: Mailbox management page now loads and displays mailboxes correctly

---

### 3. Email Authentication Issue - IPv6 PTR Records (IN PROGRESS)

**Problem**: Emails sent from office@y2k.global are rejected by Gmail with IPv6 error

**Gmail Rejection Message**:
```
Gmail has detected that this message does not meet IPv6 sending guidelines
regarding PTR records and authentication
```

**Root Cause**: Missing IPv6 reverse DNS (PTR) record for `2a01:239:28a:4100::1`

**Current Status**:
- ✓ SPF Record: Configured (`v=spf1 mx a -all`)
- ✓ DKIM Record: Configured and enabled
- ✓ DMARC Record: Configured (`v=DMARC1; p=quarantine;...`)
- ✗ IPv6 PTR Record: **MISSING** (This is the current blocking issue)

**Solution**: Configure IPv6 PTR record via hosting provider

See [IPV6_PTR_SETUP.md](./IPV6_PTR_SETUP.md) for detailed setup instructions

---

## DNS Records Configuration

### Essential Records (REQUIRED) - Add These First

#### 1. A Record (Mail Server)
```
Type:  A
Name:  mail
Value: 82.165.141.243
TTL:   3600
```
Routes `mail.y2k.global` to the mail server IP address.

#### 2. MX Record (Mail Exchange - CRITICAL)
```
Type:     MX
Name:     @ (root domain)
Value:    mail.y2k.global
Priority: 10
TTL:      3600
```
**Critical**: Without this, no external mail servers will attempt to deliver email to your domain.

#### 3. SPF Record (Sender Policy Framework - CRITICAL)
```
Type:  TXT
Name:  @ (root domain)
Value: v=spf1 mx a -all
TTL:   3600
```
This tells receiving mail servers (Gmail, Outlook, etc.):
- Only servers authorized by the MX record can send mail
- Only servers with the A record IP (82.165.141.243) can send mail
- All other servers are rejected (`-all` policy)

---

### Authentication Records

#### 4. DKIM Record (DomainKeys Identified Mail - REQUIRED for Gmail)
```
Type:  TXT
Name:  dkim._domainkey
Value: v=DKIM1; k=rsa; p=<public-key-from-mailcow-admin>
TTL:   3600
```

**How to Generate DKIM Key**:
1. Log in to Mailcow admin: https://mail.y2k.global/admin/
2. Navigate to **Configuration → DKIM**
3. Click **Add DKIM**
4. Select domain: `y2k.global`
5. Use default selector: `dkim`
6. Key size: 2048 (or 4096)
7. Click **Add** to generate
8. Copy the public key (starts with `v=DKIM1; k=rsa; p=...`)
9. Paste into DNS record value

#### 5. DMARC Record (Optional but Recommended)
```
Type:  TXT
Name:  _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:postmaster@y2k.global
TTL:   3600
```
This helps prevent email spoofing and provides delivery failure reports.

---

### Optional Email Client Records

#### Autodiscover (for Outlook auto-configuration)
```
CNAME  autoconfig     mail.y2k.global
CNAME  autodiscover   mail.y2k.global
```

---

## Implementation Checklist

- [ ] **Step 1**: Add A record (`mail.y2k.global` → `82.165.141.243`)
- [ ] **Step 2**: Add MX record (`@` → `mail.y2k.global` priority 10)
- [ ] **Step 3**: Add SPF record (`@` → `v=spf1 mx a -all`)
- [ ] **Step 4**: Generate DKIM in Mailcow admin panel
- [ ] **Step 5**: Add DKIM TXT record (`dkim._domainkey`)
- [ ] **Step 6**: Add DMARC record (`_dmarc`) - optional
- [ ] **Step 7**: Wait 15-30 minutes for DNS propagation
- [ ] **Step 8**: Test email delivery to Gmail

---

## Email Authentication Troubleshooting

### Validate DNS Records

```bash
# Check MX record
dig y2k.global MX

# Check SPF record
dig y2k.global TXT

# Check DKIM record
dig dkim._domainkey.y2k.global TXT

# Check A record
dig mail.y2k.global A
```

### Online Validation Tools
- **SPF Validator**: https://www.mxtoolbox.com/spf.aspx
- **DKIM Checker**: https://www.mxtoolbox.com/dkim.aspx
- **Google MX Toolbox**: https://toolbox.googleapps.com/apps/checkmx/
- **All-in-one**: https://mxtoolbox.com/

### Common Issues

1. **SPF Record Not Found**
   - Check that TXT record is on root domain `@` not `y2k.global`
   - Wait for DNS propagation (15-30 minutes)

2. **DKIM Public Key Format**
   - Must start with `v=DKIM1; k=rsa; p=`
   - No extra spaces or line breaks
   - Selector must match what Mailcow generated (usually `dkim`)

3. **MX Record Not Resolving**
   - Run `dig y2k.global MX` to verify
   - Check priority value (should be `10`)
   - Value should be `mail.y2k.global` (with trailing dot in some systems)

---

## Email Authentication & IPv6 PTR Setup

### Current Email Authentication Status

Your mail server has the following authentication methods configured:

| Check | Status | Details |
|-------|--------|---------|
| **MX Record** | ✓ Configured | `@` → `mail.y2k.global` priority 10 |
| **A Record (IPv4)** | ✓ Configured | `mail.y2k.global` → `82.165.141.243` |
| **SPF Record** | ✓ Configured | `v=spf1 mx a -all` |
| **DKIM Record** | ✓ Configured | Public key in DNS |
| **DMARC Record** | ✓ Configured | `v=DMARC1; p=quarantine;...` |
| **IPv6 PTR Record** | ⚠ **PENDING** | **`2a01:239:28a:4100::1` → `mail.y2k.global`** |

### Why IPv6 PTR Record Matters

Gmail and other major email providers now validate IPv6 reverse DNS (PTR) records as part of email sender reputation checks. Without this record, emails may be rejected with:

```
Gmail has detected that this message does not meet IPv6 sending guidelines
regarding PTR records and authentication
```

### Server Information

- **IPv4 Address**: 82.165.141.243
- **IPv6 Address**: 2a01:239:28a:4100::1
- **Mail Hostname**: mail.y2k.global
- **Domain**: y2k.global
- **Hosting Provider**: Strato.de

### IPv6 PTR Record Configuration - Quick Steps

#### Step 1: Contact Hosting Provider

Log into your Strato control panel:
1. Go to **https://www.strato.de/** and login
2. Navigate to **"Meine Server"** (My Servers)
3. Find your server (IP: 82.165.141.243)
4. Look for **"Reverse DNS"** or **"PTR Records"** option

#### Step 2: Configure IPv6 PTR Record

Set the following:

| Parameter | Value |
|-----------|-------|
| IPv6 Address | `2a01:239:28a:4100::1` |
| PTR Target | `mail.y2k.global` |

Also set IPv4 PTR for consistency:

| Parameter | Value |
|-----------|-------|
| IPv4 Address | `82.165.141.243` |
| PTR Target | `mail.y2k.global` |

#### Step 3: Wait for Propagation

- **Initial propagation**: 5-15 minutes
- **Full propagation**: Up to 24-48 hours

#### Step 4: Verify Configuration

**Using Online Tools:**
- Go to **https://mxtoolbox.com/ReverseLookup.aspx**
- Enter: `2a01:239:28a:4100::1`
- Should return: `mail.y2k.global`

**Using Command Line:**
```bash
# Check IPv6 PTR record
dig -x 2a01:239:28a:4100::1
# or
host 2a01:239:28a:4100::1
```

#### Step 5: Test Email Delivery

1. Send a test email from office@y2k.global to a Gmail account
2. Open the email in Gmail
3. Click **⋮** (three dots) → **"Show original"**
4. Look for authentication headers:
   - `SPF: PASS` ✓
   - `DKIM: PASS` ✓
   - `DMARC: PASS` ✓

### Strato Support Template

If you need to contact Strato support:

```
Subject: Configure IPv6 Reverse DNS (PTR) Record

Hello,

I need to configure reverse DNS (PTR) records for my mail server:

Server Details:
- IPv4 Address: 82.165.141.243
- IPv6 Address: 2a01:239:28a:4100::1
- Target Hostname: mail.y2k.global

Please set:
- IPv6 PTR (2a01:239:28a:4100::1) → mail.y2k.global
- IPv4 PTR (82.165.141.243) → mail.y2k.global

This is needed for proper email authentication compliance.
```

**Strato Support Contact:**
- **Phone**: +49 30 300 146 0 (Germany)
- **Email**: support@strato.de
- **Portal**: https://www.strato.de/

---

## Branding & Customization

### Y2K Custom Branding Setup

The Mailcow mail server and SOGo webmail interface have been branded with the Y2K Global logo and custom color scheme.

### Logo Files

- **Admin Panel**: `/opt/mailcow-dockerized/data/web/img/custom/logo.png` (29 KB)
- **Webmail (SOGo)**: `/opt/mailcow-dockerized/data/conf/sogo/custom/logo.png` (29 KB)

### Branding Color Scheme

Y2K Global colors:
- **Primary Dark**: #0f3460 (Dark Blue - headers, borders)
- **Primary Darker**: #1a1a2e & #16213e (Gradients)
- **Secondary**: #533483 (Purple - accent on hover states)
- **Accent**: #ff6b35 (Orange - highlights and links)

### Branding Files Location

```
/opt/mailcow-dockerized/
├── data/
│   ├── web/
│   │   ├── img/custom/
│   │   │   └── logo.png
│   │   └── css/
│   │       └── custom-branding.css
│   └── conf/sogo/
│       ├── custom/
│       │   ├── logo.png
│       │   └── branding.css
│       └── GNUstepDefaults.in
```

### Accessing Branded Interfaces

- **Admin Panel**: https://mail.y2k.global/admin/
  - Features Y2K logo in header
  - Custom dark blue gradient navbar
  - Orange accent colors on interactive elements

- **Webmail (SOGo)**: https://webmail.y2k.global/ or https://mail.y2k.global/SOGo/
  - Features Y2K logo on login page
  - Dark gradient background
  - White login container with Y2K color accents

### Update Branding

#### Replace Logo

```bash
# Update logo files (maintain same filename)
cp new_logo.png /opt/mailcow-dockerized/data/web/img/custom/logo.png
cp new_logo.png /opt/mailcow-dockerized/data/conf/sogo/custom/logo.png

# Restart affected containers
cd /opt/mailcow-dockerized
docker-compose restart php-fpm-mailcow sogo-mailcow nginx-mailcow
```

#### Update Colors

Edit the CSS files:
- Mailcow Admin: `/opt/mailcow-dockerized/data/web/css/custom-branding.css`
- SOGo Webmail: `/opt/mailcow-dockerized/data/conf/sogo/custom/branding.css`

Then restart containers:
```bash
cd /opt/mailcow-dockerized
docker-compose restart php-fpm-mailcow sogo-mailcow nginx-mailcow
```

#### Update Organization Name

Edit SOGo configuration:
```bash
nano /opt/mailcow-dockerized/data/conf/sogo/GNUstepDefaults.in
# Change: OrganizationName = "Y2K Global";

# Restart SOGo
docker-compose restart sogo-mailcow
```

### Browser Caching

If changes don't appear immediately:
1. Clear browser cache (Ctrl+Shift+Del)
2. Do a hard refresh (Ctrl+F5)
3. Try in an incognito/private window

---

## Management & Troubleshooting

### View Mailcow Logs
```bash
cd /opt/mailcow-dockerized
docker-compose logs -f
```

### View Specific Container Logs
```bash
# Mail submission (Postfix)
docker logs mailcowdockerized-postfix-mailcow-1 -f

# Mail delivery (Dovecot)
docker logs mailcowdockerized-dovecot-mailcow-1 -f

# Email authentication (Rspamd)
docker logs mailcowdockerized-rspamd-mailcow-1 -f

# Web interface (PHP-FPM)
docker logs mailcowdockerized-php-fpm-mailcow-1 -f
```

### Container Status
```bash
# List all containers
docker ps | grep mailcow

# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Restart Services
```bash
cd /opt/mailcow-dockerized

# Restart specific container
docker-compose restart postfix-mailcow

# Restart entire Mailcow
docker-compose restart

# Full stop and start
docker-compose down
docker-compose up -d
```

### Database Access
```bash
# Access MySQL
cd /opt/mailcow-dockerized
docker exec -it mailcowdockerized-mysql-mailcow-1 mysql -umailcow -p

# List mailboxes
SELECT username, domain FROM mailbox;

# Check mailbox storage
SELECT username, bytes FROM mailbox;

# List domains
SELECT domain FROM domain;
```

### Update Mailcow
```bash
cd /opt/mailcow-dockerized
./update.sh
```

### Backup & Restore
```bash
cd /opt/mailcow-dockerized

# Backup everything
./helper-scripts/backup_and_restore.sh backup all

# Backup specific domain
./helper-scripts/backup_and_restore.sh backup domain y2k.global

# List backups
ls backups/
```

---

## Docker Containers Running

All 18+ Mailcow containers should be running:
- `nginx-mailcow` - Reverse proxy (internal)
- `postfix-mailcow` - SMTP (mail submission/delivery)
- `dovecot-mailcow` - IMAP/POP3 (mailbox access)
- `mysql-mailcow` - Database
- `redis-mailcow` - Cache
- `rspamd-mailcow` - Email filtering & authentication
- `clamd-mailcow` - Antivirus scanning
- `php-fpm-mailcow` - Web interface backend
- `sogo-mailcow` - Webmail (SOGo)
- `dockerapi-mailcow` - Docker API wrapper
- `memcached-mailcow` - Additional cache
- `unbound-mailcow` - DNS resolver
- `netfilter-mailcow` - Network filtering
- `watchdog-mailcow` - Health monitoring
- `acme-mailcow` - SSL certificate management
- `ofelia-mailcow` - Task scheduler
- `postfix-tlspol-mailcow` - TLS policy
- `olefy-mailcow` - Ole file processor

Check status:
```bash
docker ps --filter "label=com.docker.compose.project=mailcowdockerized"
```

---

## API Access

Use Mailcow's REST API for programmatic management:

### Get API Key (from admin panel)
1. Login to https://mail.y2k.global/admin/
2. Go to **Configuration → API**
3. Generate or view API key

### Example API Calls
```bash
# List all domains
curl -X GET https://mail.y2k.global/api/v1/get/domain/all \
  -H "X-API-Key: YOUR_API_KEY"

# List all mailboxes
curl -X GET https://mail.y2k.global/api/v1/get/mailbox/all \
  -H "X-API-Key: YOUR_API_KEY"

# Get mailbox details
curl -X GET https://mail.y2k.global/api/v1/get/mailbox/office@y2k.global \
  -H "X-API-Key: YOUR_API_KEY"

# Create mailbox
curl -X POST https://mail.y2k.global/api/v1/add/mailbox \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser@y2k.global",
    "password": "SecurePassword123!",
    "password2": "SecurePassword123!",
    "quota": 3221225472,
    "active": 1
  }'
```

API Documentation: https://docs.mailcow.email/api/

---

## Important Notes

1. **Admin Password**: Changed from default `moohoo` to `Admin2025!`
2. **Old Setup Removed**: Previous PostfixAdmin setup has been completely removed
3. **Docker-based**: All mail services run in Docker containers
4. **Automatic SSL**: Let's Encrypt certificate for mail.y2k.global is managed by Mailcow
5. **SMTP Port 25**: Open for incoming mail, restricted outbound by ISP
6. **Port 465/587**: For authenticated mail submission

---

## Testing Email Delivery

### Send Test Email
1. Create mailbox in Mailcow admin
2. Login to SOGo webmail: https://webmail.y2k.global/
3. Send email to external address (gmail.com)
4. Check delivery and authentication headers

### Check Email Headers (Gmail)
1. Open received email in Gmail
2. Click "Show original" to view full email headers
3. Look for:
   - `SPF: PASS`
   - `DKIM: PASS`
   - `DMARC: PASS`

---

## Helpful Links

- **Mailcow Documentation**: https://docs.mailcow.email/
- **Docker Compose Reference**: https://docs.docker.com/compose/
- **SPF Record Syntax**: https://tools.ietf.org/html/rfc7208
- **DKIM Specification**: https://tools.ietf.org/html/rfc6376
- **DMARC Specification**: https://tools.ietf.org/html/rfc7489

---

## Support & Troubleshooting

### Where to Find Logs
- Mailcow Docker logs: `docker-compose logs`
- Nginx proxy logs: `/var/log/nginx/error.log` and `/var/log/nginx/access.log`
- Postfix logs: `docker logs mailcowdockerized-postfix-mailcow-1`

### Common Problems

**Issue**: Cannot login to admin panel
- **Solution**: Verify password, check if PHP-FPM container is running

**Issue**: Emails not being delivered
- **Solution**: Check MX record, verify DNS propagation, check Postfix logs

**Issue**: Webmail not loading
- **Solution**: Check SOGo container status, clear browser cache, check Nginx logs

**Issue**: DKIM/SPF validation failing
- **Solution**: Regenerate DKIM in admin panel, verify DNS record format, check DNS propagation

---

**Last Updated**: 2025-10-22
**Status**: Active & Operational ✓
