import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email, subject, body, config):
    """
    Send email using SMTP configuration
    """
    if not config.get('smtp_host') or not config.get('smtp_user'):
        raise ValueError("Email configuration is incomplete")
    
    msg = MIMEMultipart()
    msg['From'] = config.get('from_email', config.get('smtp_user'))
    msg['To'] = to_email
    msg['Subject'] = f"[ESB-NAS] {subject}"
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP(config['smtp_host'], config.get('smtp_port', 587))
        server.starttls()
        server.login(config['smtp_user'], config['smtp_password'])
        text = msg.as_string()
        server.sendmail(config.get('from_email', config['smtp_user']), to_email, text)
        server.quit()
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
