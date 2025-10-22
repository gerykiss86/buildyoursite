#!/usr/bin/env python3
"""
Reset admin password directly via SSH/Docker exec
"""

import subprocess
import bcrypt

password = "Admin2025!"
salt = bcrypt.gensalt(rounds=10)
hash_obj = bcrypt.hashpw(password.encode('utf-8'), salt)
bcrypt_hash = hash_obj.decode('utf-8')
mailcow_hash = "{BLF-CRYPT}" + bcrypt_hash

print(f"Password: {password}")
print(f"Hash: {mailcow_hash}")

# Use SSH to connect and update
ssh_host = "82.165.141.243"
ssh_key = "C:\\temp\\ssh\\waywiser\\private.ppk"

# Create the SQL command
sql_cmd = f"UPDATE admin SET password = '{mailcow_hash}' WHERE username = 'admin';"

# Run via plink
cmd = [
    "plink",
    "-i", ssh_key,
    f"root@{ssh_host}",
    f"cd /opt/mailcow-dockerized && docker exec mailcowdockerized-mysql-mailcow-1 mysql -umailcow -pQDnQlWsXGXc07JiovdM0yYBhWy6f mailcow -e \"{sql_cmd}\""
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    print(f"Result: {result.returncode}")
    if result.stdout:
        print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Error: {result.stderr}")
except Exception as e:
    print(f"Failed: {e}")

# Verify
print("\n--- Verification ---")
verify_cmd = [
    "plink",
    "-i", ssh_key,
    f"root@{ssh_host}",
    "cd /opt/mailcow-dockerized && docker exec mailcowdockerized-mysql-mailcow-1 mysql -umailcow -pQDnQlWsXGXc07JiovdM0yYBhWy6f mailcow -e \"SELECT password FROM admin WHERE username='admin';\""
]

try:
    result = subprocess.run(verify_cmd, capture_output=True, text=True, timeout=30)
    print(f"Stored hash:\n{result.stdout}")
except Exception as e:
    print(f"Verification failed: {e}")
