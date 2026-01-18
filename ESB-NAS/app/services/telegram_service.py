import requests


def send_telegram(chat_id, message, config):
    """
    Send message via Telegram Bot API
    """
    if not config.get('bot_token'):
        raise ValueError("Telegram bot token is not configured")
    
    url = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        error_info = response.json().get('description', 'Unknown error')
        raise Exception(f"Failed to send Telegram message: {error_info}")
    
    return response.json().get('result', {}).get('message_id')
