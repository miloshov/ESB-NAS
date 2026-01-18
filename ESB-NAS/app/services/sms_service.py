import re
import requests


def normalize_phone(phone):
    """
    Normalize phone number to E.164 format
    - Remove all non-digit characters except leading +
    - Ensure number starts with + for E.164 format
    """
    if not phone:
        return None
    
    # Strip whitespace
    phone = phone.strip()
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # If already has + prefix, preserve it
    if phone.startswith('+'):
        return '+' + digits
    
    # If it's a 10-15 digit number without country code, add + (assuming US)
    # For international numbers, user should include country code
    if len(digits) >= 10 and len(digits) <= 15:
        return '+' + digits
    
    return phone


def send_sms(to_phone, subject, body, config):
    """
    Send SMS using Twilio or generic HTTP API
    """
    provider = config.get('provider', 'twilio')
    
    # Normalize phone number
    to_phone = normalize_phone(to_phone)
    
    if provider == 'twilio':
        return send_twilio(to_phone, subject, body, config)
    else:
        raise ValueError(f"Unsupported SMS provider: {provider}")


def send_twilio(to_phone, subject, body, config):
    """
    Send SMS using Twilio API
    """
    if not config.get('account_sid') or not config.get('auth_token') or not config.get('from_number'):
        raise ValueError("Twilio configuration is incomplete")
    
    # Check if we have the Twilio library, otherwise use HTTP
    try:
        from twilio.rest import Client
        
        client = Client(config['account_sid'], config['auth_token'])
        message = client.messages.create(
            body=f"[ESB-NAS] {subject}\n{body}",
            from_=config['from_number'],
            to=to_phone
        )
        return message.sid
    except ImportError:
        # Fallback to direct HTTP request
        url = f"https://api.twilio.com/2010-04-01/Accounts/{config['account_sid']}/Messages.json"
        auth = (config['account_sid'], config['auth_token'])
        data = {
            'To': to_phone,
            'From': config['from_number'],
            'Body': f"[ESB-NAS] {subject}\n{body}"
        }
        
        response = requests.post(url, auth=auth, data=data)
        if response.status_code != 201:
            raise Exception(f"Failed to send SMS: {response.text}")
        
        return response.json().get('sid')
