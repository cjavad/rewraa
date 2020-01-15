# Copyright (c) 2017 Javad Shafique All rigths reserved

"""
This python program compiles the source of the program into
a single pyx file and then converts it to c code that executes python code!.
this does not make the program that faster but it creates some security for the source code.
"""

# VARIBLES
OUTFILE = "rewraa.pyx" # file to output to
SETUP = True # to include main.py
BASE_DIR = "../src/" # dir for all files

# Banned lines of code (Modules)
BANNED_MODULES = [
    "import sys\n",
    "from os import _exit, environ\n"
    "from .lib.rsa import rsa as RSA\n"
    "from .lib import aes as AES\n"
    "from .lib import tools as st\n",
    "from .lib.colors import color\n",
    "import os\n"
]

# Copyrigth notice
NOTICES = ["# Copyright (c) 2017 Javad Shafique All rigths reserved\n\n"]
# modules to be imported
MODULES = ["import random\n", "import threading\n", "import socket\n", "import string\n"]
# Code that is needed in the start of the file for compatibility
CODE = ["\n", "sys = os.sys\n", "_exit = os._exit\n", "environ = os.environ\n"]
# Files to read
LIB_FILES = ["lib/aes.py", "lib/rsa.py", "lib/colors.py", "lib/tools.py"]
FILES = ["client.py", "server.py"]

# add setup
if SETUP:
    END = list()
    DAT = open("main.py", "r").readlines()
    for i in DAT:
        if i.split(" ")[0] in ("import", "from") and not i in MODULES:
            MODULES.append(i)
        else:
            END.append(i)
else:
    END = [""]

# READ FILES

for FILE in LIB_FILES:
    # from base dir
    FILE = BASE_DIR + FILE
    # read file
    data = open(FILE, "r").readlines()
    # first add a start line
    CODE.append("\n\n# " + FILE + " START #\n\n")
    # run over each line
    for line in data:
        # if it's an import stament
        if line.split(" ")[0] in ("import", "from"):
            # remove comment
            line = line.split("#")[0]
            # and add to Module list if it isn't there already
            if not line in MODULES:
                MODULES.append(line)
            # else pass
            else:
                pass
        # if it isn't a module
        else:
            # add to code list
            CODE.append(line)
    # add a next comment
    CODE.append("\n\n# " + FILE + " END #\n\n")

# code for client and server
# using a seprate one for understandebilyty (or something)
WCODE = list()

# for each file in files
for FILE in FILES:
    # read from base dir
    FILE = BASE_DIR + FILE
    data = open(FILE, "r").readlines()
    # add start stament
    WCODE.append("\n\n# " + FILE + " START #\n\n")
    # and run over lines
    for line in data:
        # if it's an import statment
        if line.split(" ")[0] in ("import", "from"):
            # dont use them cause you know
            # all in one (other modules is already imported)
            pass
        else:
            # else add to wcode
            WCODE.append(line)
    # add end statment
    WCODE.append("\n\n# " + FILE + " END #\n\n")

# check if there is any problems with the code
for c, i in enumerate(MODULES):
    if i[len(i) - 1] != "\n":
        MODULES[c] = i[:-1] + "\n"

# combine all the code
LIST = NOTICES + MODULES + CODE + WCODE + END

# and write it to the outfile
with open(OUTFILE, "w") as F:
    for i in LIST:
        F.write(i)
