import os
import platform

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


Pyinstaller_location = find("pyinstaller.exe","/")

print(Pyinstaller_location)

if platform.system().upper() == "WINDOWS":
    command = Pyinstaller_location + ' --collect-all sv_ttk --add-data="docs/*;docs" -F UI.py'
if platform.system().upper() == "DARWIN":
    command = Pyinstaller_location + ' --collect-all sv_ttk --add-data="docs/*:docs" -F UI.py'

os.system(command)

if platform.system().upper() == "WINDOWS":
    os.system("rmdir /s /q build")
    os.system("del UI.spec")
if platform.system().upper() == "DARWIN":
    os.system("rm -r build")
    os.system("rm UI.spec")
