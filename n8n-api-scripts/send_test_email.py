"""Send test email to trigger n8n workflow"""
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

# Test company data
test_company_data = """
Company Name: TechInnovate Solutions GmbH
Industry: Software Development & IT Consulting
Location: Vienna, Austria

Services:
- Custom Software Development
- Cloud Infrastructure Solutions
- Digital Transformation Consulting
- Mobile App Development
- AI & Machine Learning Integration

About:
TechInnovate Solutions is a cutting-edge technology company specializing in delivering innovative software solutions to businesses across Europe. Founded in 2015, we have grown to become a trusted partner for companies looking to leverage technology for competitive advantage.

Our team of 50+ experienced developers, architects, and consultants work collaboratively to transform ideas into powerful digital solutions. We pride ourselves on our agile approach, technical excellence, and commitment to client success.

Core Values:
- Innovation First
- Client-Centric Approach
- Technical Excellence
- Continuous Learning
- Sustainable Growth

Contact:
Email: contact@techinnovate.at
Phone: +43 1 234 5678
Address: Stephansplatz 1, 1010 Vienna, Austria

Website Requirements:
- Modern, professional design
- Mobile responsive
- Showcase our services and expertise
- Include client testimonials section
- Contact form integration
- Blog/News section for updates
"""

print("=" * 60)
print("SENDING TEST EMAIL TO TRIGGER N8N WORKFLOW")
print("=" * 60)

# Create message
msg = MIMEMultipart('alternative')
msg['Subject'] = f"generate website - Test {datetime.now().strftime('%H:%M:%S')}"
msg['From'] = smtp_from
msg['To'] = 'info@kiss-it.io'  # n8n monitored inbox

# Create text and HTML versions
text_body = test_company_data

html_body = f"""
<html>
<head></head>
<body style="font-family: Arial, sans-serif;">
    <h2>Generate Website Request</h2>
    <pre style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
{test_company_data}
    </pre>
    <hr>
    <p><em>This is an automated test email sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
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

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        print("Connected to SMTP server")

        print("Starting TLS...")
        server.starttls()

        print(f"Authenticating as {smtp_user}...")
        server.login(smtp_user, smtp_password)

        print(f"Sending test email to info@kiss-it.io...")
        server.send_message(msg)

        print("\n[SUCCESS] Test email sent!")
        print(f"Subject: {msg['Subject']}")
        print(f"To: {msg['To']}")
        print("\nThe n8n workflow should be triggered shortly.")
        print("Check the workflow execution at: https://n8n.getmybot.pro")

except Exception as e:
    print(f"\n[ERROR] Failed to send email: {e}")