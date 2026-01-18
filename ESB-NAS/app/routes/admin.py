from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Template, Recipient, Integration, AlertLog, User, SystemSettings
import json

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
def dashboard():
    templates_count = Template.query.count()
    recipients_count = Recipient.query.count()
    recent_logs = AlertLog.query.order_by(AlertLog.created_at.desc()).limit(10).all()
    return render_template('admin.html', 
                         templates_count=templates_count,
                         recipients_count=recipients_count,
                         recent_logs=recent_logs)


# Template Management
@admin_bp.route('/templates', methods=['GET', 'POST'])
@login_required
def templates():
    # Handle POST actions (add, edit from forms)
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            template = Template(
                title=request.form.get('title'),
                content=request.form.get('content'),
                severity=request.form.get('severity', 'warning')
            )
            db.session.add(template)
        
        elif action == 'edit':
            template_id = request.form.get('template_id')
            template = Template.query.get_or_404(template_id)
            template.title = request.form.get('title')
            template.content = request.form.get('content')
            template.severity = request.form.get('severity', 'warning')
        
        elif action == 'delete':
            template_id = request.form.get('template_id')
            template = Template.query.get_or_404(template_id)
            db.session.delete(template)
        
        elif action == 'toggle':
            template_id = request.form.get('template_id')
            template = Template.query.get_or_404(template_id)
            template.is_active = not template.is_active
        
        db.session.commit()
        return redirect(url_for('admin.templates'))
    
    templates = Template.query.order_by(Template.created_at.desc()).all()
    return render_template('admin_templates.html', templates=templates)


# Toggle template status
@admin_bp.route('/templates/toggle/<int:template_id>', methods=['POST'])
@login_required
def toggle_template(template_id):
    template = Template.query.get_or_404(template_id)
    template.is_active = not template.is_active
    db.session.commit()
    return redirect(url_for('admin.templates'))


# Delete template
@admin_bp.route('/templates/delete/<int:template_id>', methods=['POST'])
@login_required
def delete_template(template_id):
    template = Template.query.get_or_404(template_id)
    db.session.delete(template)
    db.session.commit()
    return redirect(url_for('admin.templates'))


# Recipient Management
@admin_bp.route('/recipients', methods=['GET', 'POST'])
@login_required
def recipients():
    # Handle POST actions (add, edit from forms)
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            recipient = Recipient(
                name=request.form.get('name'),
                email=request.form.get('email') or None,
                phone=request.form.get('phone') or None,
                telegram_chat_id=request.form.get('telegram_chat_id') or None,
                slack_channel=request.form.get('slack_channel') or None
            )
            db.session.add(recipient)
        
        elif action == 'edit':
            recipient_id = request.form.get('recipient_id')
            recipient = Recipient.query.get_or_404(recipient_id)
            recipient.name = request.form.get('name')
            recipient.email = request.form.get('email') or None
            recipient.phone = request.form.get('phone') or None
            recipient.telegram_chat_id = request.form.get('telegram_chat_id') or None
            recipient.slack_channel = request.form.get('slack_channel') or None
        
        elif action == 'delete':
            recipient_id = request.form.get('recipient_id')
            recipient = Recipient.query.get_or_404(recipient_id)
            db.session.delete(recipient)
        
        elif action == 'toggle':
            recipient_id = request.form.get('recipient_id')
            recipient = Recipient.query.get_or_404(recipient_id)
            recipient.is_active = not recipient.is_active
        
        db.session.commit()
        return redirect(url_for('admin.recipients'))
    
    recipients = Recipient.query.order_by(Recipient.created_at.desc()).all()
    return render_template('admin_recipients.html', recipients=recipients)


# Toggle recipient status
@admin_bp.route('/recipients/toggle/<int:recipient_id>', methods=['POST'])
@login_required
def toggle_recipient(recipient_id):
    recipient = Recipient.query.get_or_404(recipient_id)
    recipient.is_active = not recipient.is_active
    db.session.commit()
    return redirect(url_for('admin.recipients'))


# Delete recipient
@admin_bp.route('/recipients/delete/<int:recipient_id>', methods=['POST'])
@login_required
def delete_recipient(recipient_id):
    recipient = Recipient.query.get_or_404(recipient_id)
    db.session.delete(recipient)
    db.session.commit()
    return redirect(url_for('admin.recipients'))


# Integration Management
@admin_bp.route('/integrations', methods=['GET', 'POST'])
@login_required
def integrations():
    if request.method == 'POST':
        service_type = request.form.get('service_type')
        config = {}
        
        if service_type == 'email':
            config = {
                'smtp_host': request.form.get('smtp_host'),
                'smtp_port': int(request.form.get('smtp_port', 587)),
                'smtp_user': request.form.get('smtp_user'),
                'smtp_password': request.form.get('smtp_password'),
                'from_email': request.form.get('from_email'),
                'use_tls': True
            }
        elif service_type == 'sms':
            config = {
                'provider': request.form.get('sms_provider', 'twilio'),
                'account_sid': request.form.get('account_sid'),
                'auth_token': request.form.get('auth_token'),
                'from_number': request.form.get('from_number')
            }
        elif service_type == 'telegram':
            config = {
                'bot_token': request.form.get('bot_token'),
                'default_chat_id': request.form.get('default_chat_id')
            }
        elif service_type == 'slack':
            config = {
                'webhook_url': request.form.get('webhook_url') or None,
                'bot_token': request.form.get('bot_token') or None
            }
            # Remove None values
            config = {k: v for k, v in config.items() if v}
        
        integration = Integration.query.filter_by(service_type=service_type).first()
        if not integration:
            integration = Integration(service_type=service_type)
            db.session.add(integration)
        
        integration.config_json = json.dumps(config)
        integration.is_enabled = 'is_enabled' in request.form
        db.session.commit()
        
        return redirect(url_for('admin.integrations'))
    
    integrations = {}
    for service_type in ['email', 'sms', 'telegram', 'slack']:
        integration = Integration.query.filter_by(service_type=service_type).first()
        if integration:
            config = json.loads(integration.config_json or '{}')
            integrations[service_type] = {**config, 'is_enabled': integration.is_enabled}
        else:
            integrations[service_type] = {'is_enabled': False}
    
    return render_template('admin_integrations.html', integrations=integrations)


# Test Integrations
@admin_bp.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    if request.method == 'POST':
        service_type = request.form.get('service_type')
        test_results = {}
        
        from app.services.email_service import send_email
        from app.services.sms_service import send_sms
        from app.services.telegram_service import send_telegram
        from app.services.slack_service import send_slack
        
        integration = Integration.query.filter_by(service_type=service_type, is_enabled=True).first()
        if not integration:
            return jsonify({'success': False, 'message': f'{service_type} integration not configured or disabled'})
        
        config = json.loads(integration.config_json or '{}')
        
        try:
            if service_type == 'email':
                test_email = request.form.get('test_email')
                send_email(test_email, 'Test Message', 'This is a test message from ESB-NAS', config)
                test_results['email'] = 'Email sent successfully'
            
            elif service_type == 'sms':
                test_phone = request.form.get('test_phone')
                send_sms(test_phone, 'Test', 'This is a test message from ESB-NAS', config)
                test_results['sms'] = 'SMS sent successfully'
            
            elif service_type == 'telegram':
                test_chat_id = request.form.get('test_chat_id') or config.get('default_chat_id')
                send_telegram(test_chat_id, 'This is a test message from ESB-NAS', config)
                test_results['telegram'] = 'Telegram message sent successfully'
            
            elif service_type == 'slack':
                test_channel = request.form.get('test_channel')
                send_slack(test_channel, 'This is a test message from ESB-NAS', config)
                test_results['slack'] = 'Slack message sent successfully'
            
            return jsonify({'success': True, 'message': 'Test completed', 'results': test_results})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    integrations = Integration.query.all()
    return render_template('admin_test.html', integrations=integrations)


@admin_bp.route('/telegram-test')
@login_required
def telegram_test():
    """Telegram direct test page"""
    return render_template('admin_telegram_test.html')


@admin_bp.route('/test-telegram-direct', methods=['POST'])
@login_required
def test_telegram_direct():
    """Direct Telegram test with custom chat_id"""
    data = request.get_json()
    bot_token = data.get('bot_token')
    chat_id = data.get('chat_id')
    message = data.get('message', 'Test message from ESB-NAS')
    
    if not bot_token:
        return jsonify({'success': False, 'message': 'Bot token is required'})
    
    if not chat_id:
        return jsonify({'success': False, 'message': 'Chat ID is required'})
    
    try:
        import requests
        
        # First, verify the bot token
        verify_url = f"https://api.telegram.org/bot{bot_token}/getMe"
        verify_resp = requests.get(verify_url)
        
        if verify_resp.status_code != 200:
            return jsonify({
                'success': False, 
                'message': 'Invalid bot token',
                'details': verify_resp.json().get('description', 'Unknown error')
            })
        
        bot_info = verify_resp.json().get('result', {})
        bot_name = bot_info.get('first_name', 'Unknown')
        
        # Try to send a message
        send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        send_resp = requests.post(send_url, json=payload)
        send_data = send_resp.json()
        
        if send_resp.status_code == 200:
            return jsonify({
                'success': True,
                'message': f'Message sent to {chat_id}',
                'bot_name': bot_name,
                'result': send_data.get('result', {})
            })
        else:
            error_desc = send_data.get('description', 'Unknown error')
            return jsonify({
                'success': False,
                'message': f'Failed to send message: {error_desc}',
                'error_code': send_data.get('error_code'),
                'bot_name': bot_name,
                'chat_id_used': chat_id,
                'tip': 'Make sure the bot is added to the chat/group and the chat ID is correct. For groups, use @myidbot to get the correct group ID.'
            })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


# Change Password
@admin_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if new_password != confirm_password:
        return jsonify({'success': False, 'message': 'New passwords do not match'})
    
    if not current_user.check_password(current_password):
        return jsonify({'success': False, 'message': 'Current password is incorrect'})
    
    current_user.set_password(new_password)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Password changed successfully'})


# Logs
@admin_bp.route('/logs')
@login_required
def logs():
    logs = AlertLog.query.order_by(AlertLog.created_at.desc()).all()
    return render_template('admin_logs.html', logs=logs)
