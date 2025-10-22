#!/usr/bin/env python3
"""
Generate Mailcow-format password hash
"""

import bcrypt

password = "Admin2025!"
salt = bcrypt.gensalt(rounds=10)
hash_obj = bcrypt.hashpw(password.encode('utf-8'), salt)
bcrypt_hash = hash_obj.decode('utf-8')
mailcow_hash = "{BLF-CRYPT}" + bcrypt_hash

print(f"Password: {password}")
print(f"Mailcow Hash: {mailcow_hash}")
print(f"\nSQL Command:")
print(f'UPDATE admin SET password = \'{mailcow_hash}\' WHERE username = \'admin\';')
