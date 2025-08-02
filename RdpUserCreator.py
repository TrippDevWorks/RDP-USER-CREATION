# TrippDev.xyz - RDP User Creator
# This script creates a new user for people to rdp with.

# importing libraries
import subprocess
import os
import datetime
import ctypes
import sys
from colorama import init, Fore, Style
from win32com.client import Dispatch
init(autoreset=True) # setting up colorama/fore colors

# All the print functions

def timestamp():  # returns the format we use for the timestamps in the console as hour:minute:second
    return f"{Fore.YELLOW}[{datetime.datetime.now().strftime('%H:%M:%S')}]" 

def startprint(): # the print that we use at the start!!!
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + Style.BRIGHT + "TrippDev.xyz")
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "RDP User Creator\n")

def getinput(prompt): # we use this to get inputs from the user, promt var shows the user what we need them to input
    return input(f"{timestamp()} {Fore.WHITE}[Input] {prompt}{Fore.LIGHTGREEN_EX}")

def successprint(msg, data="None Provided."): # used to print when we successfully did sm, allows for data parm to show info the user should store
    if data == "None Provided.":
        print(f"{timestamp()} {Fore.GREEN}[TaskRunner] {msg}")
    else:
        print(f"{timestamp()} {Fore.GREEN}[TaskRunner] {msg}: {Fore.YELLOW}{data}")

def infoprint(msg): # template for info messages!!!
    print(f"{timestamp()} {Fore.LIGHTBLUE_EX}[Info] {msg}")

def warningprint(msg): # template for warning messages!!!
    print(f"{timestamp()} {Fore.YELLOW}[Warn] {msg}")

def errorprint(msg): # template for error messages!!!
    print(f"{timestamp()} {Fore.RED}[TaskHandler] {msg}")
    input(f"{timestamp()} {Fore.RED}[Error] Press Enter to exit...")
    sys.exit(1)

def exitprint(msg): # template for when we finish, this closes the script
    infoprint(msg)
    input(f"{timestamp()} {Fore.GREEN}[TaskHandler] Press Enter to exit...")
    sys.exit(1)

# Functions used for more than 1 section of the script

def run(cmd): # runs command in a command prompt
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def checkrdpexe(): # we are checking if the rdp.exe file exists on the desktop or OneDrive Desktop, if not we will download it
    desktop_paths = [
        os.path.join(os.environ["USERPROFILE"], "Desktop", "rdp.exe"),
        os.path.join(os.environ["USERPROFILE"], "OneDrive", "Desktop", "rdp.exe"),
    ]

    for path in desktop_paths:
        if os.path.exists(path):
            return True 
    return False

# Functions used at launch of the script

def admincheck(): # used to check if the script is being run as admin         
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False

    if not is_admin:
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        if ret <= 32:
            print("Failed to elevate privileges.")
        return False

    return True

    
# SECTION 1 | Functions to fully setup rdp wrapper
def install_rdpexe(): 
    print(f"{Fore.LIGHTBLUE_EX}This section is a work in progress, please check back later for updates.")
    return False

def install_wrapper():
    print(f"{Fore.LIGHTBLUE_EX}This section is a work in progress, please check back later for updates.")
    return False

def install_ini():
    print(f"{Fore.LIGHTBLUE_EX}This section is a work in progress, please check back later for updates.")
    return False

def checkrdpdir(): 
    print(f"{Fore.LIGHTBLUE_EX}This section is a work in progress, please check back later for updates.")
    return False

def checkini(): 
    print(f"{Fore.LIGHTBLUE_EX}This section is a work in progress, please check back later for updates.")
    return False

def section1main(): 

    infoprint("If you see something isn't found just ignore it, its for debug purposes.")

    if not checkrdpexe():
        warningprint("rdp.exe not found on your desktop")
        result = getinput("Do you want to download rdp.exe? (yes/no): ").strip().lower()
        if result == "yes": 
            install_rdpexe()
        else:
            exitprint("To rdp, you need rdp.exe to easily access the rdp sessions and this program relies on it to create shortcuts to open rdp windows easily.")
    
    if not checkrdpdir():
        warningprint("RDP Wrapper directory not found.")
        result = getinput("Do you want to install RDP Wrapper? (yes/no): ").strip().lower()
        if result == "yes":
            install_wrapper()
        else:
            exitprint("To rdp, you need rdp wrapper to allow ur computer to rdp into itself multiple times and at all.")

    if not checkini():
        warningprint("RDP Wrapper configuration file not found.")
        result = getinput("Do you want to install the RDP Wrapper configuration file? (yes/no): ").strip().lower()
        if result == "yes":
            install_ini()
        else:
            exitprint("To rdp, you need the .ini file to configure the wrapper to launch rdp sessions properly.")
    
    

# SECTION 2 | Functions to get a list of users and their passwords that were made with this script

def section2main(): # gets the stored users and their passwords 
    folder_path = os.path.join(os.environ["LOCALAPPDATA"], "trippdev.xyz")
    file_path = os.path.join(folder_path, "RdpCreatorUsers.txt")

    if not os.path.exists(file_path):
        errorprint("No users found. Please create a user first.")
        exitprint("Exiting...")
    
    with open(file_path, "r") as f:
        lines = f.readlines()

    users = [line.strip() for line in lines if line.strip()]
    output = f"{Fore.LIGHTBLUE_EX}User:Password\n--------------------\n"
    output += f"\n {Fore.LIGHTBLUE_EX}".join(users)
    print(output)
    exitprint("Exiting...")

# SECTION 3 | Functions to help the user make rdp user accounts!!!

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

def storeuser(user, password): # stores user + password in a file for them to access later on
    folder_path = os.path.join(os.environ["LOCALAPPDATA"], "trippdev.xyz")
    os.makedirs(folder_path, exist_ok=True) 
    file_path = os.path.join(folder_path, "RdpCreatorUsers.txt")

    with open(file_path, "a") as f:
        f.write(f"{user}:{password}\n")
    return True

def section3main():

    if not admincheck():
        errorprint("This program must be run as administrator.")

    if not checkrdpexe(): # im changing this error print later on when i finish section 1
        errorprint("rdp.exe not found on your desktop! you can download it from https://raw.githubusercontent.com/TrippDevWorks/RDP-USER-CREATION-DOWNLOADS/main/rdp.exe")

    username = getinput("What do you want the user of your account to be called: ")
    password = getinput("What do you want the password of your account to be: ")

    if not run(["net", "user", username, password, "/add"]):
        errorprint(f"Could not create user '{username}'")

    successprint("Successfully created Account", f"{username} | {password}")

    if not run(["net", "localgroup", "Remote Desktop Users", username, "/add"]):
        errorprint(f"Could not add '{username}' to Remote Desktop Users")

    successprint("Successfully added to Remote Desktop Users group.")
    storeuser(username, password)

    if createshortcut(username, password):
        successprint("Successfully created rdp shortcut for profile", username)

    exitprint("If you change the password of the account, you need to change the password in the shortcut ( /p: variable ) or delete the entire user in computer manmagement and run this.")


if __name__ == "__main__":
    if not admincheck():
        errorprint("This program must be run as administrator.")

    startcolor = Fore.GREEN
    startprint()
    print(f"{startcolor} 1. Setup RDP | Not Finished - No functionallity")
    print(f"{startcolor} 2. List Created RDP Users + Passwords")
    print(f"{startcolor} 3. Create RDP User")
    input_choice = getinput("Please select an option (1-3): ")
    if input_choice == "1":
        section1main()
    elif input_choice == "2":
        section2main()
    elif input_choice == "3":
        section3main()
    else:
        errorprint("Invalid choice. Please rerun the script and select a valid option (1-3).")
        exitprint("Exiting...")
