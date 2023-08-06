import sys
import shutil
import getpass
import time
from tqdm import tqdm as pb
import py_telegram
import os

args = sys.argv


class module_uninstaller:
    class FNFE0(OSError):
        pass

    def uninstall():
        print("Telegram Bot Library Module Uninstaller")
        print("***************************************")
        print()

        try:
            try:
                pathforpackages = sys.prefix + "/Lib/site-packages/"
            except FileNotFoundError:
                pathforpackages = sys.prefix + "/lib/site-packages/"
            finally:
                raise module_uninstaller.FNFE0(
                    "There was an error. Please create an issue on GitHub with a note of the error code (FNFE0)")
                time.sleep(3)
                raise

            print("Do you really want to uninstall this module?")
            ok = input("(y/n): ")

            if ok == "y":
                progressbar = pb(range(2), desc="Uninstalling Module")
                progressbar.update(1)
                shutil.rmtree(pathforpackages + "py_telegram")
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
        helpdocspath = py_telegram.__file__.replace(
            "__init__.py", "helpdocs.txt")
        helpdocsfile = open(helpdocspath, "r")
        helpdocs = helpdocsfile.read()
        helpdocsfile.close()
        print(helpdocs)

    if args[1] == "--uninstall":
        module_uninstaller.uninstall()
