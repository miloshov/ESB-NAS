"""
ESB-NAS (Emergency Notification Alert System)
Main entry point for the standalone application
"""

import sys
import os
import traceback

def main():
    try:
        from app import create_app
        from config import HOST, PORT, DEBUG, DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD
        from app.models import db, User

        app = create_app()

        def create_default_admin():
            """Create default admin user if not exists"""
            with app.app_context():
                db.create_all()
                admin = User.query.filter_by(username=DEFAULT_ADMIN_USERNAME).first()
                if not admin:
                    admin = User(username=DEFAULT_ADMIN_USERNAME, is_admin=True)
                    admin.set_password(DEFAULT_ADMIN_PASSWORD)
                    db.session.add(admin)
                    db.session.commit()
                    print(f"[OK] Default admin user created: {DEFAULT_ADMIN_USERNAME}")
                else:
                    print(f"[OK] Admin user already exists: {DEFAULT_ADMIN_USERNAME}")

        print("=" * 60)
        print("  ESB-NAS - Emergency Notification Alert System")
        print("=" * 60)
        print()
        
        create_default_admin()
        
        print()
        print(f"[INFO] Server starting on http://{HOST}:{PORT}")
        print(f"[INFO] Access from network: http://[YOUR_IP]:{PORT}")
        print()
        print("[INFO] Default credentials:")
        print(f"       Username: {DEFAULT_ADMIN_USERNAME}")
        print(f"       Password: {DEFAULT_ADMIN_PASSWORD}")
        print()
        print("[INFO] Press Ctrl+C to stop the server")
        print("=" * 60)
        
        if DEBUG:
            app.run(host=HOST, port=PORT, debug=True)
        else:
            try:
                from waitress import serve
                serve(app, host=HOST, port=PORT)
            except ImportError:
                print("[WARNING] waitress not available, using Flask dev server")
                app.run(host=HOST, port=PORT, debug=False)
                
    except Exception as e:
        print()
        print("=" * 60)
        print("[ERROR] Application failed to start!")
        print("=" * 60)
        print()
        print("Error details:")
        print(traceback.format_exc())
        print()
        print("=" * 60)
        print("Press Enter to exit...")
        input()

if __name__ == '__main__':
    main()
