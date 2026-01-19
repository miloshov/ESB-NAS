# ESB-NAS (Emergency Notification Alert System) v0.15

**Version:** 0.15 (Clean Build based on commit 953c74c)
**Build Date:** January 18, 2026
**Status:** ✅ Stable Release - Last working configuration

A standalone web application for sending urgent emergency alerts to multiple channels simultaneously via Email, SMS, Telegram, and Slack.

## 📋 Version History

### v0.15 (January 18, 2026) - Clean Build ✅
- **Status:** Stable Release
- **Base Commit:** 953c74c (last working configuration)
- **Changes:** Clean build based on proven working version
- **Fixes:** SMS phone number normalization, logging improvements, Slack Bot Token support

### ⚠️ Known Issue with v0.15+ Builds
Subsequent commits after 953c74c introduced build process changes that may have affected stability. This version represents the last known working configuration.

## 🚀 Quick Start - Download Standalone .exe

**No Python required!** Download the ready-to-use Windows executable:

1. Go to [Releases](https://github.com/miloshov/ESB-NAS/releases)
2. Download the latest `ESB-NAS-Windows.exe`
3. Extract and run!

## Features

- 🚨 **Instant Alert Broadcasting** - Send emergency messages with a single click
- 📧 **Multi-Channel Delivery** - Email, SMS, Telegram, and Slack support
- 🌐 **Multi-Language Support** - English, Ukrainian, Serbian, and Bulgarian
- 🌓 **Dark/Light Theme** - Easy on the eyes in any environment
- 👥 **Recipient Management** - Add and manage notification recipients
- 📝 **Template System** - Pre-configured alert templates for quick deployment
- 🔒 **Admin Security** - Password-protected admin panel
- 📊 **Activity Logging** - Track all sent alerts and their status
- 🏠 **Standalone Operation** - Runs on local network, no cloud dependencies

## Getting Started

### Option 1: Download Standalone Executable (Recommended)

1. Download `ESB-NAS-Windows.exe` from [Releases](https://github.com/miloshov/ESB-NAS/releases)
2. Extract the ZIP file
3. Double-click `ESB-NAS.exe` to run
4. Open browser at `http://localhost:5000`
5. Login with: `admin` / `admin123`

### Option 2: Run with Python (For Development)

```bash
git clone https://github.com/miloshov/ESB-NAS.git
cd ESB-NAS
pip install -r requirements.txt
python run.py
```

Then access at http://localhost:5000

## Default Login

- **Username:** admin
- **Password:** admin123

⚠️ **Change the default password on first login!**

## Building Standalone Executable

To build the Windows .exe yourself:

1. Install Python 3.10+ from https://python.org
2. Open Command Prompt in the ESB-NAS folder
3. Run: `build.bat`
4. The executable will be in `dist\ESB-NAS.exe`

Or use the automated build: push to main branch and download from [Releases](https://github.com/miloshov/ESB-NAS/releases)

## Configuration

### Email Integration (SMTP)

Configure your email provider in Admin → Integrations:

| Parameter | Description | Example |
|-----------|-------------|---------|
| SMTP Host | Email server hostname | smtp.gmail.com |
| SMTP Port | Server port (usually 587) | 587 |
| SMTP Username | Your email address | your@email.com |
| SMTP Password | App token or password | *********** |
| From Email | Sender email address | alerts@company.com |

### SMS Integration (Twilio)

1. Create a Twilio account at https://twilio.com
2. Get your Account SID and Auth Token
3. Purchase a phone number
4. Configure in Admin → Integrations:

| Parameter | Description | Example |
|-----------|-------------|---------|
| Account SID | Twilio account identifier | ACxxxxxxxxxxxxxxxx |
| Auth Token | Twilio authentication token | *********** |
| From Number | Your Twilio phone number | +1234567890 |

### Telegram Integration

1. Message @BotFather on Telegram
2. Create a new bot with /newbot command
3. Get your Bot Token
4. Get your Chat ID (message @userinfobot)
5. Configure in Admin → Integrations:

| Parameter | Description | Example |
|-----------|-------------|---------|
| Bot Token | Telegram bot token | 123456:ABC-DEF... |
| Default Chat ID | Default recipient chat ID | 123456789 |

### Slack Integration

1. Create a Slack App at https://api.slack.com/apps
2. Enable Incoming Webhooks
3. Create a webhook for your channel
4. Configure in Admin → Integrations:

| Parameter | Description | Example |
|-----------|-------------|---------|
| Webhook URL | Slack incoming webhook URL | https://hooks.slack.com/... |

## Usage

### Sending an Alert

1. Open the main page
2. Select an alert template from the dropdown
3. Review the number of active recipients
4. Press the red ALERT button
5. Confirm the action

### Managing Templates

In Admin → Templates, you can:
- Add new alert templates
- Edit existing templates
- Set severity level (Info, Warning, Critical)
- Enable/disable templates
- Delete templates

### Managing Recipients

In Admin → Recipients, you can:
- Add recipients with their contact information
- Specify which channels each recipient should receive alerts on
- Enable/disable recipients
- Delete recipients

## Project Structure

```
ESB-NAS/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── routes/
│   │   ├── main.py          # Main routes (home, send alert)
│   │   └── admin.py         # Admin routes
│   ├── services/
│   │   ├── email_service.py # Email sending logic
│   │   ├── sms_service.py   # SMS sending logic
│   │   ├── telegram_service.py
│   │   └── slack_service.py
│   ├── static/
│   │   ├── css/style.css    # Styling
│   │   └── js/app.js        # Frontend JavaScript
│   └── templates/           # HTML templates
├── database/                # SQLite database storage
├── translations/            # Language files
├── .github/workflows/       # CI/CD for auto-build
├── esb-nas.spec             # PyInstaller configuration
├── build.bat                # Windows build script
├── config.py                # Configuration
├── run.py                   # Application entry point
├── run.bat                  # Windows launcher
└── requirements.txt         # Python dependencies
```

## Deployment

### Local Network

The application is accessible from all devices on the same network:

- Local access: `http://localhost:5000`
- Network access: `http://[SERVER_IP]:5000`

### Production Deployment

For production use, consider:

1. **Use a production WSGI server:** The standalone executable uses Waitress by default
2. **Set environment variables:**
   ```bash
   export SECRET_KEY='your-secure-random-key'
   ```
3. **Consider a reverse proxy** (Nginx, Apache) for SSL termination

## API Endpoints

### Main Routes
- `GET /` - Main alert page
- `POST /send-alert` - Send alert notification
- `POST /set-language` - Set interface language
- `POST /set-theme` - Set theme (dark/light)
- `GET /login` - Admin login page
- `POST /login` - Login submission
- `GET /logout` - Logout

### Admin Routes
- `GET /admin/` - Dashboard
- `GET /admin/templates` - Template management
- `POST /admin/templates` - Add/edit/delete templates
- `GET /admin/recipients` - Recipient management
- `POST /admin/recipients` - Add/edit/delete recipients
- `GET /admin/integrations` - Integration configuration
- `POST /admin/integrations` - Save integration settings
- `GET /admin/test` - Integration testing page
- `POST /admin/test` - Test integration
- `POST /admin/change-password` - Change admin password

## Security Considerations

1. **Change default credentials** immediately after first login
2. **Use strong passwords** for the admin account
3. **Keep API keys secure** - don't share them
4. **Run on secure networks** when possible
5. **Consider HTTPS** for production deployments
6. **Restrict access** to the admin panel if needed

## Troubleshooting

### Port already in use

Windows:
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Database issues

Delete the database file:
```cmd
del database\esb_nas.db
ESB-NAS.exe
```

### Integration not working

1. Check integration settings in Admin → Integrations
2. Verify API keys and tokens are correct
3. Test integrations using Admin → Test page
4. Check console logs for error messages

## License

This project is open source and available under the MIT License.

## Support

For issues and feature requests, please open an issue on GitHub.
