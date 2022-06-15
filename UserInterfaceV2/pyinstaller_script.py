import os
import platform

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


if platform.system().upper() == "WINDOWS":
    Pyinstaller_location = find("pyinstaller.exe","/")
    command = Pyinstaller_location + ' --collect-all sv_ttk --add-data="docs/*;docs" -F UI_V2.py'
if platform.system().upper() == "DARWIN":
    command = 'pyinstaller --collect-all sv_ttk --add-data="docs/*:docs" -F UI_V2.py'

os.system(command)

if platform.system().upper() == "WINDOWS":
    os.system("rmdir /s /q build")
    os.system("del UI_V2.spec")
if platform.system().upper() == "DARWIN":
    os.system("rm -r build")
    os.system("rm UI_V2.spec")

    
