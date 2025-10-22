#!/usr/bin/env python3
"""
Generate bcrypt hash for admin password
"""

import bcrypt

password = "Admin2025!"
salt = bcrypt.gensalt(rounds=10)
hash_obj = bcrypt.hashpw(password.encode('utf-8'), salt)
hash_str = hash_obj.decode('utf-8')

print(f"Password: {password}")
print(f"Bcrypt Hash: {hash_str}")
print(f"\nUse this in SQL:")
print(f"UPDATE admin SET password = '{hash_str}' WHERE username = 'admin';")
