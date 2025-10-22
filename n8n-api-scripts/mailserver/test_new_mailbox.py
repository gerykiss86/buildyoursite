#!/usr/bin/env python3
"""
Test the newly created mailbox
"""

import smtplib
import imaplib

print("=" * 60)
print("Testing New Mailbox Authentication")
print("=" * 60)

email = "newtest@y2k.global"
password = "NewTest2025!"

# Test SMTP
print("\nTesting SMTP...")
try:
    smtp = smtplib.SMTP('mail.y2k.global', 587)
    smtp.starttls()
    smtp.login(email, password)
    print("[OK] SMTP authentication successful!")
    smtp.quit()
except Exception as e:
    print(f"[FAIL] SMTP authentication failed: {e}")

# Test IMAP
print("\nTesting IMAP...")
try:
    imap = imaplib.IMAP4_SSL('mail.y2k.global', 993)
    imap.login(email, password)
    print("[OK] IMAP authentication successful!")
    imap.logout()
except Exception as e:
    print(f"[FAIL] IMAP authentication failed: {e}")

print("\n" + "=" * 60)