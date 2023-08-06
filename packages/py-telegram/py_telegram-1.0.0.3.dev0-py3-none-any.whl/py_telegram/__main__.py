import sys
import shutil
import getpass
import time
from tqdm import tqdm as pb
import py_telegram
import os

args = sys.argv


class module_uninstaller:
    def uninstall():
        print("Telegram Bot Library Module Uninstaller")
        print("***************************************")
        print()

        try:

            pathforpackages = "C:/Users/" + getpass.getuser() + \
                "/AppData/Local/Programs/Python/Python38-32/Lib/site-packages/"

            print("Do you really want to uninstall this module?")
            ok = input("(y/n): ")

            if ok == "y":
                progressbar = pb(range(2), desc="Uninstalling Module")
                progressbar.update(1)
                shutil.rmtree(pathforpackages + "telegrambot")
                progressbar.update(1)
                progressbar.close()
                print("Sucessfully Uninstalled.")
                time.sleep(5)
            else:
                quit()
        except:
            print("There was an error. This could be because you don't operate Windows (10). This installer was only tested on Windows and it could raise errors in other operating systems. Please try it again or create an issue on GitHub.")


if len(args) > 1:
    if args[1] == "--help":
        print(os.getcwd())
        helpdocspath = telegrambot.__file__.replace(
            "__init__.py", "helpdocs.txt")
        helpdocsfile = open(helpdocspath, "r")
        helpdocs = helpdocsfile.read()
        helpdocsfile.close()
        print(helpdocs)

    if args[1] == "--uninstall":
        module_uninstaller.uninstall()
