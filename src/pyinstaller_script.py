import os
import platform


input_variable1 = os.environ['spec_file']
print("var1 = ", input_variable1)
input_variable2 = os.environ['spec']
print("var2 = ", input_variable2)

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


if platform.system().upper() == "WINDOWS":
    Pyinstaller_location = find("pyinstaller.exe","/")
    command = Pyinstaller_location + ' ' + input_variable1
if platform.system().upper() == "DARWIN":
    command = 'pyinstaller ' + input_variable1

os.system(command)

if platform.system().upper() == "WINDOWS":
    os.system("rmdir /s /q build")
    #os.system("del UI_V2.spec")
if platform.system().upper() == "DARWIN":
    os.system("rm -r build")
    #os.system("rm UI_V2.spec")

    
