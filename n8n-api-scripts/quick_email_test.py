"""Quick SMTP test"""
import smtplib
import os
from dotenv import load_dotenv

load_dotenv('n8n.env')

smtp_host = os.getenv('SMTP_HOST', 'smtp.easyname.com')
smtp_port = int(os.getenv('SMTP_PORT', 587))
smtp_user = os.getenv('SMTP_USER', '60164mail14')
smtp_password = os.getenv('SMTP_PASSWORD')

print(f"Testing SMTP connection to {smtp_host}:{smtp_port}")
print(f"User: {smtp_user}")

try:
    with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
        print("[OK] Connected to SMTP server")
        server.starttls()
        print("[OK] TLS enabled")
        server.login(smtp_user, smtp_password)
        print("[OK] Authentication successful")
        print("\nSMTP connection test PASSED! Email configuration is working.")
except Exception as e:
    print(f"[ERROR] SMTP test FAILED: {e}")