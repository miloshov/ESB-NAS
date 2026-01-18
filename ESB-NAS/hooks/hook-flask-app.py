# PyInstaller hook for Flask
# This ensures Flask templates and static files are included in the build

from PyInstaller.utils.hooks import collect_all

def hook(hook_api):
    # Collect all Flask data files (templates, static)
    datas, binaries, hiddenimports = collect_all('Flask')
    
    # Add them to the hook
    hook_api.add_datas(datas)
    hook_api.add_imports(*hiddenimports)
    
    # Also collect SQLAlchemy and Flask-Login
    datas2, binaries2, hiddenimports2 = collect_all('Flask-SQLAlchemy')
    hook_api.add_datas(datas2)
    hook_api.add_imports(*hiddenimports2)
    
    datas3, binaries3, hiddenimports3 = collect_all('Flask-Login')
    hook_api.add_datas(datas3)
    hook_api.add_imports(*hiddenimports3)
