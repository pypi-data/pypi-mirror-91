import shutil
import os
import getpass
import time
from tqdm import tqdm as pb
import sys

print("Telegram Bot Library Module Installer")
print("*************************************")
print()

try:
    old_cwd = os.getcwdb()

    pathforpackages = sys.prefix + "/Lib/site-packages/"

    override_ok = 0
    try:
        os.chdir(pathforpackages + "py_telegram")
        os.chdir("C:/")
        print(
            "There is already package with this name. Would you like to override it?")
        override = input("(y/n): ")
        if override == "y":
            override_ok = 1
            #shutil.rmtree(pathforpackages + "py_telegram")
        else:
            pass
    except FileNotFoundError:
        override_ok = 1

    if override_ok == 1:
        progressbar = pb(range(2), desc="Installing Module")

        old_path = old_cwd.decode()
        progressbar.update(1)
        shutil.unpack_archive(old_path + "/module.tar",
                              extract_dir=pathforpackages + "py_telegram")
        progressbar.update(1)
        progressbar.close()
        print("Sucessfully Installed.\nYou can import the module with 'import py_telegram' now\nIf you need help, simply type 'python -m py_telegram --help' to the system shell.")
        time.sleep(5)
except:
    print("There was an error. This could be because you don't operate Windows (10). This installer was only tested on Windows and it could raise errors in other operating systems. Please try it again or create an issue on GitHub.")
