import shutil
import os
from tqdm import tqdm as pb
import time
import getpass

os.chdir("C:/Users/" + getpass.getuser() + "/OneDrive/Programme, Elektronik und Projekte/Python/python-telegram-api")

files_for_archiving = ["LICENSE", "README.md", "__main__.py",
                       "__init__.py", "helpdocs.txt"]
dirs_for_archiving = ["module_file/module_uninstaller"]

pbRange = len(files_for_archiving) + len(dirs_for_archiving) + 5
progressbar = pb(range(pbRange), desc="Archiving Module")

i = 0
try:
    shutil.rmtree("module")
except:
    pass
os.mkdir("module")
progressbar.update(1)
progressbar.update(1)
for x in files_for_archiving:
    shutil.copyfile(files_for_archiving[i],
                    "module/" + files_for_archiving[i])
    i = i + 1
    progressbar.update(1)

i = 0
for x in dirs_for_archiving:
    shutil.copytree(dirs_for_archiving[i],
                    "module/" + dirs_for_archiving[i])
    i = i + 1
    progressbar.update(1)

os.remove("module.tar")
progressbar.update(1)
shutil.make_archive("module", "tar", root_dir="module/")
progressbar.update(1)
shutil.rmtree("module")
progressbar.update(1)
progressbar.close()

time.sleep(3)
