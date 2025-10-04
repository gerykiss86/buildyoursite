"""Send test email to correct n8n trigger address"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv('n8n.env')

# Email configuration
smtp_host = os.getenv('SMTP_HOST', 'smtp.easyname.com')
smtp_port = int(os.getenv('SMTP_PORT', 587))
smtp_user = os.getenv('SMTP_USER', '60164mail14')
smtp_password = os.getenv('SMTP_PASSWORD')
smtp_from = os.getenv('SMTP_FROM', 'admin@kiss-it.io')

# CORRECT n8n trigger email
n8n_trigger_email = 'office@buildyoursite.pro'  # The actual monitored inbox

# Test company data
test_company_data = """
Company Name: Alpine Digital Services
Industry: Digital Marketing & Web Development
Location: Innsbruck, Austria

Services:
- Web Design & Development
- Search Engine Optimization (SEO)
- Social Media Marketing
- Content Creation
- E-commerce Solutions
- Digital Strategy Consulting

About:
Alpine Digital Services is a premier digital agency nestled in the heart of the Austrian Alps. Since 2018, we've been helping businesses transform their online presence with cutting-edge digital solutions. Our team combines creative design with technical expertise to deliver results that exceed expectations.

We specialize in creating beautiful, functional websites that drive conversions and build brand awareness. From small local businesses to international corporations, we tailor our approach to meet each client's unique needs.

Core Values:
- Creative Excellence
- Data-Driven Results
- Client Partnership
- Sustainable Digital Growth
- Alpine Innovation Spirit

Team:
- 25+ Digital Experts
- Award-winning Designers
- Certified Google Partners
- Multilingual Support (German, English, Italian)

Contact:
Email: hello@alpinedigital.at
Phone: +43 512 987654
Address: Maria-Theresien-Straße 42, 6020 Innsbruck, Austria

Website Requirements:
- Clean, modern design with alpine aesthetics
- Portfolio showcase section
- Client testimonials
- Service pages with pricing
- Blog for SEO content
- Multi-language support (DE/EN)
- Contact forms with CRM integration
"""

print("=" * 60)
print("SENDING TEST EMAIL TO CORRECT N8N TRIGGER")
print("=" * 60)
print(f"Target Email: {n8n_trigger_email}")
print("-" * 60)

# Create message
msg = MIMEMultipart('alternative')
msg['Subject'] = f"generate website - Alpine Digital Test {datetime.now().strftime('%H:%M')}"
msg['From'] = smtp_from
msg['To'] = n8n_trigger_email  # Correct trigger address!

# Create text and HTML versions
text_body = test_company_data

html_body = f"""
<html>
<head></head>
<body style="font-family: Arial, sans-serif;">
    <h2>Generate Website Request</h2>
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <pre style="font-family: 'Courier New', monospace; white-space: pre-wrap;">
{test_company_data}
        </pre>
    </div>
    <hr style="border: 1px solid #e0e0e0;">
    <p style="color: #666; font-size: 12px;">
        <em>Automated test email sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em><br>
        <em>This should trigger the n8n buildyoursite workflow</em>
    </p>
</body>
</html>
"""

# Attach parts
part1 = MIMEText(text_body, 'plain')
part2 = MIMEText(html_body, 'html')

msg.attach(part1)
msg.attach(part2)

try:
    print(f"\nConnecting to SMTP server {smtp_host}:{smtp_port}...")

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        print("[OK] Connected to SMTP server")

        print("Starting TLS encryption...")
        server.starttls()
        print("[OK] TLS enabled")

        print(f"Authenticating as {smtp_user}...")
        server.login(smtp_user, smtp_password)
        print("[OK] Authentication successful")

        print(f"\nSending test email...")
        print(f"From: {smtp_from}")
        print(f"To: {n8n_trigger_email}")
        print(f"Subject: {msg['Subject']}")

        server.send_message(msg)

        print("\n" + "=" * 60)
        print("[SUCCESS] TEST EMAIL SENT!")
        print("=" * 60)
        print(f"\nThe email has been sent to: {n8n_trigger_email}")
        print("The n8n workflow should trigger within 1-2 minutes")
        print("\nMonitor at: https://n8n.getmybot.pro/#/executions")
        print("\nNote: The workflow will:")
        print("1. Generate a website using Bolt")
        print("2. Deploy it with Claude")
        print("3. Extract the deployment URL")
        print("4. Send confirmation emails and SMS")

except Exception as e:
    print(f"\n[ERROR] Failed to send email: {e}")
    print("\nTroubleshooting:")
    print("1. Check SMTP credentials")
    print("2. Verify network connectivity")
    print("3. Check if office@buildyoursite.pro accepts external emails")