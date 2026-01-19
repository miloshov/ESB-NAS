from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
import json
import sys
import os
import logging

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    from app.models import User
    return User.query.get(int(user_id))


def parse_json_filter(value):
    """Jinja2 filter to parse JSON strings"""
    if not value:
        return {}
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return {}


def create_app(test_config=None):
    """Application factory for ESB-NAS"""
    
    # Get the base directory where templates are located
    if getattr(sys, 'frozen', False):
        # Running as executable - templates are next to the executable
        basedir = os.path.dirname(sys.executable)
    else:
        # Running as script
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    template_path = os.path.join(basedir, 'app', 'templates')
    static_path = os.path.join(basedir, 'app', 'static')
    
    app = Flask(__name__,
                template_folder=template_path,
                static_folder=static_path)
    
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    
    if test_config is not None:
        app.config.update(test_config)
    
    # Register custom Jinja2 filters
    app.jinja_env.filters['parse_json'] = parse_json_filter
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
