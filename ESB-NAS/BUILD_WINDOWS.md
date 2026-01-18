# Standalone Windows Executable Build Instructions

## Quick Start (If Python is installed)

1. Open Command Prompt in the ESB-NAS folder
2. Run: `build.bat`
3. The executable will be created in `dist\ESB-NAS.exe`

## Build Process

The build script will:
- Install PyInstaller (if not present)
- Bundle Python interpreter
- Include all dependencies (Flask, SQLAlchemy, etc.)
- Include static files (CSS, JS, templates)
- Include translations and configuration
- Create a single `.exe` file

## Requirements for Building

- Windows 10/11
- Python 3.10 or higher
- Internet connection (for downloading dependencies)

## Output

After building, you'll get:
- `dist/ESB-NAS.exe` - Standalone executable (~50-100 MB)
- Can be copied to any Windows computer
- No Python installation required to run

## Running the Standalone Application

1. Copy `dist/ESB-NAS.exe` to any folder on any Windows PC
2. Double-click to run
3. Open browser at `http://localhost:5000`
4. Login with: `admin` / `admin123`

## Troubleshooting

### "Python is not recognized"
- Install Python from https://python.org
- **Important:** Check "Add Python to PATH" during installation
- Restart Command Prompt after installation

### Build fails with memory error
- Close other applications
- Try: `pyinstaller --clean esb-nas.spec --windowed`

### Antivirus flags the .exe
- This is normal for self-extracting executables
- Add exclusion if needed
- The source code is available on GitHub for verification
