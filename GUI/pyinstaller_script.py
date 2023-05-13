import os
import platform

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

print(platform.system())
if platform.system().upper() == "WINDOWS":
    Pyinstaller_location = find("pyinstaller.exe","/")
    command = Pyinstaller_location + ' -F GUI.py'
if platform.system().upper() == "DARWIN":
    command = 'pyinstaller -F GUI.py'
if platform.system().upper() == "LINUX":
    command = 'wine pyinstaller -F GUI.py'
os.system(command)

if platform.system().upper() == "WINDOWS":
    os.system("rmdir /s /q build")
    os.system("del GUI.spec")
if platform.system().upper() == "DARWIN":
    os.system("rm -r build")
    os.system("rm UI_V2.spec")
if platform.system().upper() == "LINUX":
    os.system("rm -r build")
    os.system("rm UI_V2.spec")
    
