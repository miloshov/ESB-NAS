import sys
import os

# PyInstaller runtime hook
# This ensures proper extraction of bundled files

def get_base_path():
    if getattr(sys, 'frozen', False):
        # Running as executable
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Set environment variables
os.environ['BASE_PATH'] = get_base_path()
