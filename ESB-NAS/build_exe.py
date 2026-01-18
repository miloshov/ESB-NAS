# Build script for ESB-NAS Windows executable

import os
import sys
import shutil
from PyInstaller.__main__ import run

# Configuration
APP_NAME = "ESB-NAS"
SOURCE_FILE = "run.py"

def build():
    print("=" * 60)
    print(f"Building {APP_NAME} Windows Executable")
    print("=" * 60)
    
    # Clean previous builds
    for folder in ['dist', 'build']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"[CLEAN] Removed {folder}/")
    
    os.makedirs('dist', exist_ok=True)
    
    # PyInstaller arguments
    args = [
        '--name', APP_NAME,
        '--onedir',           # Directory mode
        '--console',          # Show console for debugging
        '--clean',
        SOURCE_FILE
    ]
    
    print(f"[BUILD] Running PyInstaller...")
    
    try:
        run(args)
        
        # Copy data files to build output
        base_path = os.path.join('dist', APP_NAME)
        
        # Copy entire app directory
        if os.path.exists('app'):
            dest = os.path.join(base_path, 'app')
            shutil.copytree('app', dest, dirs_exist_ok=True)
            print(f"[COPY] app/ folder")
        
        # Copy translations
        if os.path.exists('translations'):
            shutil.copytree('translations', os.path.join(base_path, 'translations'), dirs_exist_ok=True)
            print(f"[COPY] translations/")
        
        # Copy config
        if os.path.exists('config.py'):
            shutil.copy('config.py', base_path)
            print(f"[COPY] config.py")
        
        print()
        print("=" * 60)
        print(f"[SUCCESS] Build: dist/{APP_NAME}/{APP_NAME}.exe")
        print("=" * 60)
        
    except Exception as e:
        print(f"[ERROR] Build failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    build()
