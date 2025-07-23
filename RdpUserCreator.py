import subprocess
import os
import datetime
import ctypes
import sys
from colorama import init, Fore, Style
from win32com.client import Dispatch

init(autoreset=True)

def timestamp():
    return f"{Fore.YELLOW}[{datetime.datetime.now().strftime('%H:%M:%S')}]"

def startprint():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + Style.BRIGHT + "TrippDev.xyz")
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "RDP User Creator\n")

def getinput(prompt):
    return input(f"{timestamp()} {Fore.WHITE}[Input] {prompt}{Fore.LIGHTGREEN_EX}")

def successprint(msg, data=""):
    print(f"{timestamp()} {Fore.GREEN}[TaskRunner] {msg}: {Fore.YELLOW}{data}")

def infoprint(msg):
    print(f"{timestamp()} {Fore.LIGHTBLUE_EX}[Info] {msg}")

def errorprint(msg):
    print(f"{timestamp()} {Fore.RED}[TaskHandler] {msg}")
    input(f"{timestamp()} {Fore.RED}[Error] Press Enter to exit...")
    sys.exit(1)

def exitprint(msg):
    infoprint(msg)
    input(f"{timestamp()} {Fore.GREEN}[TaskHandler] Press Enter to exit...")
    sys.exit(1)

def run(cmd):
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def admincheck():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def checkrdpexe():
    desktop_paths = [
        os.path.join(os.environ["USERPROFILE"], "Desktop", "rdp.exe"),
        os.path.join(os.environ["USERPROFILE"], "OneDrive", "Desktop", "rdp.exe"),
    ]

    for path in desktop_paths:
        if os.path.exists(path):
            return True 
    return False

def getuser():
    return os.getlogin()

def createshortcut(username, password):
    possible_paths = [
        os.path.join(os.environ["USERPROFILE"], "Desktop", "rdp.exe"),
        os.path.join(os.environ["USERPROFILE"], "OneDrive", "Desktop", "rdp.exe"),
    ]

    rdp_exe_path = None
    for path in possible_paths:
        if os.path.exists(path):
            rdp_exe_path = path
            break

    if not rdp_exe_path:
        raise FileNotFoundError("rdp.exe not found on Desktop or OneDrive Desktop.")

    desktop_path = os.path.dirname(rdp_exe_path)
    shortcut_path = os.path.join(desktop_path, f"{username}.lnk")

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = rdp_exe_path
    shortcut.Arguments = f'/v:127.0.0.2 /u:{username} /p:{password} /title:"{username}" /nosound /o:"keyboardhook:i:1" /w:1920 /h:1080'
    shortcut.WorkingDirectory = desktop_path
    shortcut.IconLocation = rdp_exe_path
    shortcut.save()
    return True

def main():
    startprint()

    if not admincheck():
        errorprint("This program must be run as administrator.")

    if not checkrdpexe():
        errorprint("rdp.exe not found on your desktop!")

    username = getinput("What do you want the user of your account to be called: ")
    password = getinput("What do you want the password of your account to be: ")

    if not run(["net", "user", username, password, "/add"]):
        errorprint(f"Could not create user '{username}'")

    successprint("Successfully created Account", f"{username} | {password}")

    if not run(["net", "localgroup", "Remote Desktop Users", username, "/add"]):
        errorprint(f"Could not add '{username}' to Remote Desktop Users")

    successprint("Successfully added to Remote Desktop Users group.")

    if createshortcut(username, password):
        successprint("Successfully created rdp shortcut for profile", username)

    exitprint("If you change the password of the account, you need to change the password in the shortcut ( /p: variable ) or delete the entire user in computer manmagement and run this.")

if __name__ == "__main__":
    main()
