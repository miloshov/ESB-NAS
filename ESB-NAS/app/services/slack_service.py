import requests


def send_slack(channel, message, config, severity='info'):
    """
    Send message via Slack
    Supports both Incoming Webhook and Bot Token authentication
    
    Args:
        channel: Slack channel (e.g., #alerts)
        message: Message text to send
        config: Configuration dict with webhook_url or bot_token
        severity: Alert severity (info, warning, critical) for styling
    """
    # Determine authentication method
    webhook_url = config.get('webhook_url')
    bot_token = config.get('bot_token')
    
    if webhook_url:
        return send_slack_webhook(webhook_url, channel, message, severity)
    elif bot_token:
        return send_slack_api(bot_token, channel, message, severity)
    else:
        raise ValueError("Slack is not configured. Please add webhook_url or bot_token in integration settings.")


def send_slack_webhook(webhook_url, channel, message, severity='info'):
    """Send message via Slack Incoming Webhook"""
    
    # Color based on severity
    colors = {
        'info': '#3498db',
        'warning': '#f39c12',
        'critical': '#e74c3c'
    }
    color = colors.get(severity, '#3498db')
    
    # Emoji based on severity
    emojis = {
        'info': ':information_source:',
        'warning': ':warning:',
        'critical': ':rotating_light:'
    }
    emoji = emojis.get(severity, ':information_source:')
    
    payload = {
        'channel': channel,
        'username': 'ESB-NAS Alert',
        'icon_emoji': emoji,
        'attachments': [
            {
                'color': color,
                'text': message,
                'mrkdwn_in': ['text']
            }
        ]
    }
    
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code not in [200, 204]:
        error_info = response.text if response.text else 'Unknown error'
        raise Exception(f"Failed to send Slack message: {error_info}")
    
    return True


def send_slack_api(bot_token, channel, message, severity='info'):
    """
    Send message via Slack API (Bot Token)
    Requires channels:write scope
    """
    # Color based on severity
    colors = {
        'info': '#3498db',
        'warning': '#f39c12',
        'critical': '#e74c3c'
    }
    color = colors.get(severity, '#3498db')
    
    # Emoji based on severity
    emojis = {
        'info': ':information_source:',
        'warning': ':warning:',
        'critical': ':rotating_light:'
    }
    emoji = emojis.get(severity, ':information_source:')
    
    # First, convert channel name to ID if needed
    channel_id = channel
    if channel.startswith('#'):
        channel_id = get_channel_id(bot_token, channel)
        if not channel_id:
            raise Exception(f"Channel {channel} not found or bot doesn't have access")
    
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        'Authorization': f'Bearer {bot_token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'channel': channel_id,
        'text': message,
        'username': 'ESB-NAS Alert',
        'icon_emoji': emoji,
        'attachments': [
            {
                'color': color,
                'text': message,
                'mrkdwn_in': ['text']
            }
        ]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    
    if not data.get('ok'):
        error_msg = data.get('error', 'Unknown error')
        raise Exception(f"Failed to send Slack message: {error_msg}")
    
    return True


def get_channel_id(bot_token, channel_name):
    """
    Get Slack channel ID from channel name
    Returns None if channel not found or no permission
    """
    url = "https://slack.com/api/conversations.list"
    headers = {
        'Authorization': f'Bearer {bot_token}'
    }
    
    params = {
        'types': 'public_channel,private_channel',
        'limit': 1000
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        if data.get('ok'):
            for channel in data.get('channels', []):
                if channel.get('name') == channel_name.lstrip('#'):
                    return channel.get('id')
        
        return None
    except Exception:
        return None


def test_slack_connection(config):
    """
    Test Slack connection and return status
    Returns dict with success status and details
    """
    webhook_url = config.get('webhook_url')
    bot_token = config.get('bot_token')
    
    if webhook_url:
        return test_slack_webhook(webhook_url)
    elif bot_token:
        return test_slack_api(bot_token)
    else:
        return {
            'success': False,
            'message': 'Slack is not configured. Please add webhook_url or bot_token.'
        }


def test_slack_webhook(webhook_url):
    """Test Incoming Webhook"""
    try:
        payload = {
            'text': 'Test message from ESB-NAS',
            'username': 'ESB-NAS Test',
            'icon_emoji': ':white_check_mark:'
        }
        
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code in [200, 204]:
            return {
                'success': True,
                'message': 'Slack webhook is working correctly!'
            }
        else:
            return {
                'success': False,
                'message': f'Slack webhook error: {response.text}'
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'Connection failed: {str(e)}'
        }


def test_slack_api(bot_token):
    """Test Slack Bot Token"""
    try:
        # Test auth
        url = "https://slack.com/api/auth.test"
        headers = {'Authorization': f'Bearer {bot_token}'}
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data.get('ok'):
            bot_name = data.get('bot_id', 'Unknown')
            return {
                'success': True,
                'message': f'Slack bot token is valid! (Bot ID: {bot_name})',
                'bot_name': bot_name
            }
        else:
            return {
                'success': False,
                'message': f'Auth failed: {data.get("error")}'
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'Connection failed: {str(e)}'
        }


def get_slack_channels(bot_token):
    """
    Get list of available Slack channels
    Requires conversations:read scope
    """
    url = "https://slack.com/api/conversations.list"
    headers = {
        'Authorization': f'Bearer {bot_token}'
    }
    
    params = {
        'types': 'public_channel,private_channel',
        'limit': 1000
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        if data.get('ok'):
            channels = []
            for channel in data.get('channels', []):
                channels.append({
                    'id': channel.get('id'),
                    'name': f"#{channel.get('name')}",
                    'is_private': channel.get('is_private', False)
                })
            return {
                'success': True,
                'channels': channels
            }
        else:
            return {
                'success': False,
                'message': f'Failed to get channels: {data.get("error")}',
                'channels': []
            }
    except Exception as e:
        return {
            'success': False,
            'message': str(e),
            'channels': []
        }
