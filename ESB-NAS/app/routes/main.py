from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db, logger
from app.models import Template, Recipient
import json

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    templates = Template.query.filter_by(is_active=True).all()
    recipients_count = Recipient.query.filter_by(is_active=True).count()
    
    # Convert templates to JSON-serializable format
    templates_data = [
        {
            'id': t.id,
            'title': t.title,
            'content': t.content,
            'severity': t.severity
        }
        for t in templates
    ]
    
    return render_template('index.html', templates=templates_data, recipients_count=recipients_count)


@main_bp.route('/send-alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    template_id = data.get('template_id')
    user_id = data.get('user_id', 'anonymous')
    
    if not template_id:
        return jsonify({'success': False, 'message': 'Template ID is required'}), 400
    
    template = Template.query.get_or_404(template_id)
    recipients = Recipient.query.filter_by(is_active=True).all()
    
    if not recipients:
        return jsonify({'success': False, 'message': 'No active recipients found'}), 400
    
    # Import notification services
    from app.services.email_service import send_email
    from app.services.sms_service import send_sms
    from app.services.telegram_service import send_telegram
    from app.services.slack_service import send_slack
    from app.models import Integration, AlertLog
    
    results = {
        'email': {'sent': 0, 'failed': 0, 'errors': []},
        'sms': {'sent': 0, 'failed': 0, 'errors': []},
        'telegram': {'sent': 0, 'failed': 0, 'errors': []},
        'slack': {'sent': 0, 'failed': 0, 'errors': []}
    }
    
    # Get integrations
    email_config = Integration.query.filter_by(service_type='email', is_enabled=True).first()
    sms_config = Integration.query.filter_by(service_type='sms', is_enabled=True).first()
    telegram_config = Integration.query.filter_by(service_type='telegram', is_enabled=True).first()
    slack_config = Integration.query.filter_by(service_type='slack', is_enabled=True).first()
    
    # Send emails
    if email_config:
        email_settings = json.loads(email_config.config_json or '{}')
        for recipient in recipients:
            if recipient.email:
                try:
                    send_email(
                        recipient.email, 
                        template.title, 
                        template.content,
                        email_settings
                    )
                    results['email']['sent'] += 1
                except Exception as e:
                    results['email']['failed'] += 1
                    results['email']['errors'].append(f"{recipient.email}: {str(e)}")
    
    # Send SMS
    if sms_config:
        sms_settings = json.loads(sms_config.config_json or '{}')
        logger.info(f"SMS integration enabled, processing {len([r for r in recipients if r.phone and r.phone.strip()])} recipients with phone numbers")
        for recipient in recipients:
            if recipient.phone and recipient.phone.strip():
                phone_clean = recipient.phone.strip()
                logger.info(f"Sending SMS to recipient: {recipient.name}, phone: {phone_clean}")
                try:
                    send_sms(
                        phone_clean, 
                        template.title, 
                        template.content,
                        sms_settings
                    )
                    results['sms']['sent'] += 1
                    logger.info(f"SMS sent successfully to {phone_clean}")
                except Exception as e:
                    results['sms']['failed'] += 1
                    results['sms']['errors'].append(f"{phone_clean}: {str(e)}")
                    logger.error(f"SMS failed to {phone_clean}: {str(e)}")
    
    # Send Telegram
    if telegram_config:
        telegram_settings = json.loads(telegram_config.config_json or '{}')
        for recipient in recipients:
            if recipient.telegram_chat_id:
                try:
                    send_telegram(
                        recipient.telegram_chat_id,
                        f"*{template.title}*\n\n{template.content}",
                        telegram_settings
                    )
                    results['telegram']['sent'] += 1
                except Exception as e:
                    results['telegram']['failed'] += 1
                    results['telegram']['errors'].append(f"{recipient.telegram_chat_id}: {str(e)}")
    
    # Send Slack
    if slack_config:
        slack_settings = json.loads(slack_config.config_json or '{}')
        for recipient in recipients:
            if recipient.slack_channel:
                try:
                    send_slack(
                        recipient.slack_channel,
                        f"*{template.title}*\n\n{template.content}",
                        slack_settings
                    )
                    results['slack']['sent'] += 1
                except Exception as e:
                    results['slack']['failed'] += 1
                    results['slack']['errors'].append(f"{recipient.slack_channel}: {str(e)}")
    
    # Log the alert
    alert_log = AlertLog(
        template_id=template_id,
        triggered_by=user_id,
        status_json=json.dumps(results)
    )
    db.session.add(alert_log)
    db.session.commit()
    
    total_sent = sum(r['sent'] for r in results.values())
    total_failed = sum(r['failed'] for r in results.values())
    
    return jsonify({
        'success': True,
        'message': f'Alert sent! {total_sent} successful, {total_failed} failed.',
        'results': results
    })


@main_bp.route('/set-language', methods=['POST'])
def set_language():
    data = request.get_json()
    lang = data.get('language', 'en')
    session['language'] = lang
    return jsonify({'success': True})


@main_bp.route('/set-theme', methods=['POST'])
def set_theme():
    data = request.get_json()
    theme = data.get('theme', 'dark')
    session['theme'] = theme
    return jsonify({'success': True})


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        from app.models import User
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')


@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
