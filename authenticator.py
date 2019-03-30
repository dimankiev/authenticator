try:
    import time as stime
    from mbedtls import hash as hashlib
    import sys, base64, shelve2, os, threading, configparser, datetime, uuid, traceback, re, pyotp, pyAesCrypt, os.path
    import random as rnd
    from datetime import *
    try:
        from tkinter import *
        from tkinter import ttk
        tkinter_support_status = True
    except:
        #print("Tkinter is not supported or not installed !\nGUI is disabled !")
        tkinter_support_status = False
    from colorama import Fore, Style, Back, init
    from typing import List, Union
    from prompt_toolkit.shortcuts import prompt
    from prompt_toolkit.styles import Style as pStyle
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.validation import Validator, ValidationError
except Exception as e:
    print("%s\n\nPlease, use the commands below to install required modules: " % str(e))
    print('pip install "module name that printed below"\nExample: pip install prompt_toolkit pyotp pyAesCrypt colorama\nTkinter Linux install: sudo apt-get install python3-tk')
    exit()

sr = Style.RESET_ALL
version = "1.0.2.0"

auth_prompt = PromptSession()

autoupdate_lable = "None"

class passwordValidator(Validator):
    def validate(self, document):
        text = document.text
        if text and not (len(text) > 4) or text == None or len(text) == 0:
            i = 0
            for i, c in enumerate(text):
                if not (len(text) > 4) or text == None or len(text) == 0:
                    valid_err_msg = 'The 2FA key is can\'t be less than 4 chars'
                    break

            raise ValidationError(message=valid_err_msg,
                                  cursor_position=i)

def ripemd_hash(string):
    ripemd = hashlib.new('ripemd160')
    ripemd.update(str.encode(string))
    return ripemd.hexdigest()

def bottom_toolbar():
    return [('class:bottom-toolbar', getCodeToolbar(autoupdate_lable))]

def getCodeToolbar(autoupdate_lable):
        if autoupdate_lable in authenticator.keyring:
            code = pyotp.TOTP(authenticator.keyring[autoupdate_lable]).now()
            return str("[%s] Your code is: %s" % (autoupdate_lable.upper(), code))
        else:
            return str("[HERE WILL BE SHOWN YOUR 2FA CODES]")

def initPrompt(its_password,auth,stage):
    cmd_validator = False
    cmd_style = pStyle.from_dict({
    # User input (default text).
    '':          '#ffffff',

    # Prompt.
    'username': '#21F521',
    'at':       'ansigreen',
    'colon':    '#ffffff',
    'pound':    '#ffffff',
    'host':     '#21F521', # bg:#444400
    'path':     'ansicyan underline',
    'bottom-toolbar': 'ansiblue bg:#ffffff'
    })
    if auth:
        cmd_msg = [
        ('class:at',       ''),
        ('class:host',     ""),
        ('class:colon',    ''),
        ('class:path',     ''),
        ('class:pound',    '')
        ]
        if stage == 1:
            cmd_msg.append(('class:username', "2FA (Two-factor authentication KEY: "))
            cmd_validator = passwordValidator()
        elif stage == 2:
            cmd_msg.append(('class:username', "PIN Code: "))
    else:
        cmd_msg = [
        ('class:username', "auth"),
        ('class:at',       '@'),
        ('class:host',     'aaa114-project'),
        ('class:colon',    ':'),
        ('class:path',     '~/'),
        ('class:pound',    '# ')
        ]
    data = str(auth_prompt.prompt(cmd_msg, style=cmd_style, bottom_toolbar=bottom_toolbar, refresh_interval=0.5, validator=cmd_validator, is_password=its_password, auto_suggest=AutoSuggestFromHistory()))
    if stage == 1:
        return data.lower()
    return data

init()
print(Fore.GREEN + Style.BRIGHT + "aaa114-project Authenticator v.%s" % version)

exit_mode = False #RESERVE CODE EXECUTION PREVENTION

class authenticator:
    password = ""
    keyring = {}
    def addPassword(password):
        authenticator.password = ripemd_hash(password)

if not os.path.isfile("configs/authenticator.db.enc"):
    print(Fore.YELLOW + Style.BRIGHT + "That is the first launch of that script.\nAuthenticator configuration will be saved automatically." + sr)
    print(Fore.RED + Style.BRIGHT + "Please, make your PIN to save data.")
try:
    while True:
        try:
            password = initPrompt(True,True,2).replace(" ","")
            authenticator.addPassword(password)
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + "Exiting...\n%s" % str(e) + sr)
            exit_mode = True
            traceback.print_exc()
            exit()
        if len(password) < 4 and not os.path.isfile("configs/authenticator.db.enc"):
            sol = input("PIN is too small. Generate random ?(y/n): ").lower()
            if sol == "y" or sol == "yes":
                password = str(rnd.randint(1000,9999))
                print(Fore.RED + "Your PIN: " + Style.BRIGHT + password)
            else:
                continue
        elif len(password) < 4:
            print(Fore.RED + "PIN can't be less than 4 chars")
            continue
        break
except:
    exit()

def encData(mode,password):
    global exit_mode
    bufferSize = 64 * 1024
    if mode == "encrypt":
        pyAesCrypt.encryptFile("configs/authenticator.db", "configs/authenticator.db.enc", password, bufferSize)
        try:
            os.remove("configs/authenticator.db")
        except:
            pass
    else:
        try:
            while True:
                try:
                    pyAesCrypt.decryptFile("configs/authenticator.db.enc", "configs/authenticator.db", password, bufferSize)
                except:
                    if os.path.isfile("configs/authenticator.db.enc"):
                        print(Fore.RED + Style.BRIGHT + "Code is invalid !")
                        try:
                            while True:
                                try:
                                    password = initPrompt(True,True,2).replace(" ","")
                                    authenticator.addPassword(password)
                                except:
                                    print(Fore.RED + Style.BRIGHT + "Exiting..." + sr)
                                    exit_mode = True
                                    exit()
                                if len(password) < 4:
                                    print(Fore.RED + Style.BRIGHT + "PIN can't be less than 4 chars" + sr)
                                    continue
                                else:
                                    break
                        except:
                            exit_mode = True
                            exit()
                        continue
                    else:
                        pass
                break
        except:
            exit_mode = True
            exit()
        try:
            os.remove("configs/authenticator.db.enc")
        except:
            pass

def loadData():
    try:
        encData("decrypt",password)
        data = shelve2.open("configs/authenticator")
        success_sload = 1
    except:
        success_sload = 0
        data.close()
        data = None
    return {"load": success_sload, "data": data}

def saveData(keyring):
    try:
        save = shelve2.open("configs/authenticator")
        save["keyring"] = authenticator.keyring
        save.close()
        encData("encrypt",password)
    except:
        try:
            os.mkdir("./configs")
            save = shelve2.open("configs/authenticator")
            save["keyring"] = keyring
            save.close()
            encData("encrypt",password)
        except PermissionError:
            print("Save failed ! Please check your read/write permissions\n(If you a Linux or Android user, check chmod or try to launch this script as root)")
            save.close()

def returnData():
    auth_info = {"success": True}
    try:
        data_load = loadData()
        if data_load["load"] == 1:
            auth_info = {"success": True, "keyring": data_load["data"]["keyring"]}
            data_load["data"].close()
        else:
            data_load["data"].close()
    except Exception as e:
        try:
            data_load["data"].close()
        except:
            pass
    return auth_info

def clear():
    os.system('cls' if os.name=='nt' else 'clear')
while True:
    auth_data = returnData()
    try:
        encData("encrypt",password)
    except:
        pass
    if auth_data["success"]:
        try:
            authenticator.keyring = auth_data["keyring"]
            break
        except Exception as e:
            authenticator.keyring = {}
            break
    else:
        authenticator.keyring = {}
        break
if exit_mode:
    exit()

print(Fore.YELLOW + Style.BRIGHT + "Commands:    help - show available commands\n    add <your_lable> - add new authenticator\n    remove <your_lable> - remove authenticator\n    get <your_lable> - get authenticator code\n    export <your_lable> - export 2FA Authenticator TOTP Key\n    list - list your apps registered in authenticator\n    clear - clear terminal output" + sr)

while True:
    try:
        cmd = initPrompt(False,False,0)
        if "add" in cmd:
            try:
                lable = cmd.split(" ")[1]
                key = initPrompt(False,True,1)
                if not lable in authenticator.keyring:
                    authenticator.keyring[lable] = key
                    print(Fore.GREEN + Style.BRIGHT + "Successful added %s to keyring !" % str(Fore.WHITE + lable + Fore.GREEN))
                    autoupdate_lable = lable
                else:
                    print(Fore.YELLOW + Style.BRIGHT + "%s is already exists !" % lable.upper())
            except:
                print(Fore.YELLOW + Style.BRIGHT + "Usage:\n    add <your_lable> - add new authenticator")
        elif "remove" in cmd:
            try:
                lable = cmd.split(" ")[1]
                del authenticator.keyring[lable]
                print(Fore.GREEN + Style.BRIGHT + "Successful removed %s from authenticator.keyring !" % str(Fore.WHITE + lable + Fore.GREEN))
            except:
                print(Fore.YELLOW + Style.BRIGHT + "Usage:\n    remove <your_lable> - remove authenticator")
        elif "get" in cmd:
            try:
                lable = cmd.split(" ")[1]
                autoupdate_lable = lable
                code = pyotp.TOTP(authenticator.keyring[lable]).now()
                print(Fore.BLUE + Style.BRIGHT + "[%s] Your code: %s" % (Fore.MAGENTA + lable.upper() + Fore.BLUE, Fore.WHITE + code))
            except:
                print(Fore.YELLOW + Style.BRIGHT + "Usage:\n    get <your_lable> - get authenticator code")
        elif "list" in cmd:
            try:
                print(Fore.CYAN + Style.BRIGHT + "Your apps registered in the authenticator:\n")
                for i in authenticator.keyring:
                    print(Fore.BLUE + i)
            except:
                print(Fore.RED + "Nothing was registered! Add new app 2FA key now by 'add' command.")
        elif "export" in cmd:
            try:
                lable = cmd.split(" ")[1]
                if lable in authenticator.keyring:
                    print(Fore.RED + Style.BRIGHT + "[!WARNING!]\n" + Fore.YELLOW + "That operation is unsafe !\nIf you really want to export your TOTP 2FA Key, you must enter your valid PIN code !\n" + Fore.RED + "[!WARNING!]" + sr)
                    try:
                        if ripemd_hash(initPrompt(True,True,2).replace(" ","")) == authenticator.password:
                            print(Fore.YELLOW + Style.BRIGHT + "TOTP 2FA HASH FOR %s: %s" % (lable.upper(), Fore.WHITE + authenticator.keyring[lable] + sr))
                        else:
                            print(Fore.RED + Style.BRIGHT + "Incorrect PIN ! Try again later !")
                    except:
                        print(Fore.RED + Style.BRIGHT + "Incorrect PIN ! Try again later !")
                else:
                    print(Fore.YELLOW + Style.BRIGHT + "%s is not exists in your keyring !" % lable.upper())
            except:
                print(Fore.YELLOW + Style.BRIGHT + "Usage:\n    export <your_lable> - export 2FA Authenticator TOTP Key " + Fore.RED + "[DANGEROUS]" + sr)
        elif "exit" in cmd:
            saveData(authenticator.keyring)
            print(Fore.RED + Style.BRIGHT + "Exiting..." + sr)
            exit()
        elif "clear" in cmd:
            clear()
        elif "help" in cmd:
            print(Fore.YELLOW + Style.BRIGHT + "Commands:    help - show available commands\n    add <your_lable> - add new authenticator\n    remove <your_lable> - remove authenticator\n    get <your_lable> - get authenticator code\n    list - list your apps registered in authenticator\n    clear - clear terminal output" + sr)
        else:
            print(Fore.RED + Style.BRIGHT + "Command is unrecognized !")
    except KeyboardInterrupt:
        saveData(authenticator.keyring)
        print(Fore.RED + Style.BRIGHT + "Exiting..." + sr)
        exit()