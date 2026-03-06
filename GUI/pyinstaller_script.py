"""
pyinstaller_script.py - Build Automation for IMDASH Executable Creation

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Automates creation of platform-specific executable binaries from the IMDASH
    GUI application using PyInstaller. Provides cross-platform build support with
    platform-specific command construction and automatic cleanup of build artifacts.
    
    Supports three operating systems:
    - Windows: Native PyInstaller execution
    - macOS: Direct PyInstaller execution via system PATH
    - Linux: PyInstaller execution through Wine compatibility layer
    
    Build artifacts (build directory and .spec files) are automatically removed
    after successful executable generation.
"""

import os
import platform

def find(name, path):
    """
    Recursively search directory tree for file by name.
    
    Parameters:
        name (str): Filename to find
        path (str): Root directory path for search
        
    Returns:
        str: Full path to file if found, None otherwise
    """
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

print(platform.system())

# Construct platform-specific PyInstaller command for executable generation
if platform.system().upper() == "WINDOWS":
    Pyinstaller_location = find("pyinstaller.exe","/")
    command = Pyinstaller_location + ' -F GUI.py'
elif platform.system().upper() == "DARWIN":
    # macOS: PyInstaller available in system PATH
    command = 'pyinstaller -F GUI.py'
elif platform.system().upper() == "LINUX":
    # Linux: Execute PyInstaller through Wine emulation layer
    command = 'wine pyinstaller -F GUI.py'

# Execute PyInstaller build command
os.system(command)

# Clean up build artifacts after successful executable generation
if platform.system().upper() == "WINDOWS":
    os.system("rmdir /s /q build")
    os.system("del GUI.spec")
elif platform.system().upper() == "DARWIN":
    os.system("rm -r build")
    os.system("rm UI_V2.spec")
elif platform.system().upper() == "LINUX":
    os.system("rm UI_V2.spec")
    
