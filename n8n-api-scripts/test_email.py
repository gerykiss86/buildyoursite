"""
Test SMTP Email Functionality
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('n8n.env')

def test_smtp_connection():
    """Test SMTP connection and send a test email"""

    # SMTP Configuration
    smtp_host = os.getenv('SMTP_HOST', 'smtp.easyname.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_user = os.getenv('SMTP_USER', '60164mail14')
    smtp_password = os.getenv('SMTP_PASSWORD')
    smtp_from = os.getenv('SMTP_FROM', 'admin@kiss-it.io')

    print("=" * 60)
    print("SMTP EMAIL TESTER")
    print("=" * 60)
    print(f"\nSMTP Configuration:")
    print(f"Host: {smtp_host}")
    print(f"Port: {smtp_port}")
    print(f"User: {smtp_user}")
    print(f"From: {smtp_from}")
    print("-" * 60)

    # Get recipient
    recipient = input("\nEnter recipient email (or press Enter for default): ")
    if not recipient:
        recipient = smtp_from  # Send to self as test

    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"n8n Test Email - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    msg['From'] = smtp_from
    msg['To'] = recipient

    # Email body
    text_body = f"""
    Hello,

    This is a test email from your n8n environment.

    Test Details:
    - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    - SMTP Server: {smtp_host}:{smtp_port}
    - Sent from: {smtp_from}
    - Sent to: {recipient}

    If you received this email, your SMTP configuration is working correctly!

    Best regards,
    n8n Email Tester
    """

    html_body = f"""
    <html>
    <head></head>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #ff6d5a;">n8n Test Email</h2>
        <p>This is a <strong>test email</strong> from your n8n environment.</p>

        <h3>Test Details:</h3>
        <ul>
            <li><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            <li><strong>SMTP Server:</strong> {smtp_host}:{smtp_port}</li>
            <li><strong>Sent from:</strong> {smtp_from}</li>
            <li><strong>Sent to:</strong> {recipient}</li>
        </ul>

        <p style="background-color: #e8f5e9; padding: 10px; border-radius: 5px;">
            ✅ If you received this email, your SMTP configuration is working correctly!
        </p>

        <p>Best regards,<br>
        <em>n8n Email Tester</em></p>
    </body>
    </html>
    """

    # Attach parts
    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
        print("\n🔄 Connecting to SMTP server...")

        # Connect to server
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            print("✅ Connected to SMTP server")

            # Start TLS
            print("🔒 Starting TLS encryption...")
            server.starttls()
            print("✅ TLS enabled")

            # Login
            print(f"🔑 Authenticating as {smtp_user}...")
            server.login(smtp_user, smtp_password)
            print("✅ Authentication successful")

            # Send email
            print(f"📧 Sending email to {recipient}...")
            server.send_message(msg)
            print("✅ Email sent successfully!")

            return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("Please check your username and password.")
        return False

    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def send_custom_email():
    """Send a custom email"""
    smtp_host = os.getenv('SMTP_HOST', 'smtp.easyname.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_user = os.getenv('SMTP_USER', '60164mail14')
    smtp_password = os.getenv('SMTP_PASSWORD')
    smtp_from = os.getenv('SMTP_FROM', 'admin@kiss-it.io')

    print("\n📝 Compose Custom Email")
    print("-" * 40)

    recipient = input("To: ")
    subject = input("Subject: ")
    print("Body (type 'END' on a new line to finish):")

    lines = []
    while True:
        line = input()
        if line == 'END':
            break
        lines.append(line)

    body = '\n'.join(lines)

    # Create message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_from
    msg['To'] = recipient

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            print("✅ Custom email sent successfully!")
            return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def main():
    """Main function"""
    while True:
        print("\n" + "=" * 60)
        print("EMAIL FUNCTIONALITY TESTER")
        print("=" * 60)
        print("\nOptions:")
        print("1. Test SMTP connection (send test email)")
        print("2. Send custom email")
        print("3. View SMTP configuration")
        print("0. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            test_smtp_connection()
        elif choice == "2":
            send_custom_email()
        elif choice == "3":
            print("\nCurrent SMTP Configuration:")
            print(f"Host: {os.getenv('SMTP_HOST')}")
            print(f"Port: {os.getenv('SMTP_PORT')}")
            print(f"User: {os.getenv('SMTP_USER')}")
            print(f"From: {os.getenv('SMTP_FROM')}")
            print(f"Security: {os.getenv('SMTP_SECURE')}")
        elif choice == "0":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()