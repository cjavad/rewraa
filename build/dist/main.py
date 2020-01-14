import os
import time
import platform
import json
import operator
from difflib import SequenceMatcher

# THIS FILE WILL BE INJECTED INTO THE REWRAA.PYX

# VARIABLES

# info variables
__version__ = "1.6.1"
__module__ = "RewRaa " + __version__
__author__ = " Javad Shafique "
# Fancy license
__license__ = "Copyrigth (c) 2017-present" + __author__ + "All rigths reserved"

# a dict with command line arguments
COMMAND_ARGS = {
    "--help": [
        str(__module__ + " " + __license__),
        "\nUsage: ",
        "For server: ",
        "   rewraa server port (host, port)",
        "For client: ",
        "   rewraa host, port useColors? username\n",  
        "This program can run in five modes: ",
        "Mode 1: Setup, here it's all interactive. No arguments",
        "Mode 2: Quick, if you pass one argument either 'server' or the hostname of the computer you want to connect to",
        "Mode 3: Custom, The first argument is the same as in Quick but now you can pass a port as the second argument",
        "Mode 4: Full, Same as custom but the arguments for server is passed like this ('server', host, port) and the client (host, port, useColors?)",
        "Mode 5: Quiet, This mode is the same as full but takes one last argument the username for the client so as this (host, port, useColors?, name)",
        "",
        "Some other modes comming up:\n ",
        "rewraa hosting: starts a server with the PORT environ variable",
        "rewraa filename.rewraa: reads file as json and tries to get port, host, and username from it\n",
        "Use --help (/help, /?) to get this message\nUse --version (-v) to get the version of this program\nUse --license (/license) to get the license\nUse --author for the note left by the author\n\n",
        "NOTE: All modes using client that isn't Quiet ask for a username. Mode 2 with server listens on port 7777, the server does not take input\n"
    ],
    "--version": [
        # print package name (which includes version)
        # __version__ should only contain the version
        str(__package__)
    ],
    "--author": [
        str(__author__)
    ],
    "--license":[
        str(__license__)
    ]
}

COMMAND_ALIASES = {
    # with support for aliases
    "/help": COMMAND_ARGS["--help"],
    "/?": COMMAND_ARGS["--help"],
    "-v": COMMAND_ARGS["--version"],
    "/license":COMMAND_ARGS["--license"]
}

# ascii banner from http://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=RewRaa
BANNER = """
██████╗ ███████╗██╗    ██╗██████╗  █████╗  █████╗ 
██╔══██╗██╔════╝██║    ██║██╔══██╗██╔══██╗██╔══██╗
██████╔╝█████╗  ██║ █╗ ██║██████╔╝███████║███████║
██╔══██╗██╔══╝  ██║███╗██║██╔══██╗██╔══██║██╔══██║
██║  ██║███████╗╚███╔███╔╝██║  ██║██║  ██║██║  ██║
╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝                                               
"""

COLOR_WARNING = "WARNING: this system does not seem to support colors"


# from django.core.management.color.supports_color at https://github.com/django/django/blob/master/django/core/management/color.py
# checks if terminal supports colors. so all color support is now automatic
def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = os.sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(os.sys.stdout, 'isatty') and os.sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True

"""
Find match for wrong arguments (so cool)
"""
def find_match(string):
    stats = dict()
    strings = dict()
    keys = dict(COMMAND_ARGS, **COMMAND_ALIASES).keys()
    for c,i in enumerate(keys):
        s = SequenceMatcher(None, string, i).ratio()
        stats[str(c)] = s
        strings[str(c)] = i
    
    e = max(stats.items(), key=operator.itemgetter(1))[0]
    return strings[e]

"""
Setup if no arguments is specified
and you want to use it interativly
"""

def setup():
    # print banner
    print(BANNER)
    t = input("Start server or client? [S/c]: ")

    if t.lower() in ("s", "server"):
        # launch server
        port = int(input("Which port to listen on (7777): ") or 7777)
        host = "0.0.0.0"
        Server(port, dict(host=host or "localhost")).main()

    elif t.lower() in ("c", "client"):
        # launch client
        host = input("Ip adress of server: ")
        port = int(input("Which port to listen to (7777): ") or 7777)
        # check if system/terminal supports color
        colors = supports_color()

        # IF/ELSE it all day
        if colors:
            # take input yes is bigger
            c = input("Use colors [Y/n]:")
            # set varible accordingly
            if c.lower()[:1] == "n":
                colors = False
            else:
                colors = True

        else:
            # if support_color() returns false print warning
            print(COLOR_WARNING)
            # take input no is bigger
            c = input("Use colors [y/N]:")
            # set varible accordingly
            if c.lower()[:1] == "y":
                colors = True 
            else:
                colors = False
        # get username
        name = input("Type Username: ")
        # start client
        Client(name, host, dict(port=port, colors=colors)).main()
    
    # if the input did not choose either of
    # them count down to 0 and start again.
    else:
        # throw error
        print("Wrong choice")
        i = 10
        while i > 0:
            print(i)
            time.sleep(1)
            i = i - 1
        
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() in ("Linux", "Darwin") or os.name == "posix":
            os.system("clear")
        setup()

"""
Main function that checks amount of arguments and exectutes acordingly
"""

def main(args = None):
    if args != None:
        args = args
    else:
        args = os.sys.argv[1:]
    
    if len(args) == 0:
        setup()


    # If there only is one argument it can either be a command or one
    # of the following arguments: 
    #
    # server: starts a server on port 7777
    # $hostname: connects to the host on port 7777
    # ${filename}.rewraa: reads file as json (client only)
    # hosting: takes envionment variable PORT and listens on 0.0.0.0


    if len(args) == 1:
        # first check if it's a command
        if args[0] in COMMAND_ARGS or args[0] in COMMAND_ALIASES:
            if args[0] in COMMAND_ARGS:
                C = COMMAND_ARGS
            else:
                C = COMMAND_ALIASES
            
            for item in C[args[0]]:
                print(item)
            exit()
        if args[0][0] in ("-", "/"):
            print("Command line argument \"" + args[0] + "\" does not exist. Did you maybe mean " + find_match(args[0]))
            exit()

        # check if it's a file
        if args[0].split(".").pop() == "rewraa" and os.path.exists(args[0]):
            # load data from file
            data = json.loads(open(args[0], "r", encoding="utf-8").read())
            # read data
            port = data["port"]
            host = data["host"]
            name = data["name"]
            colors = data["colors"]
            # and start client
            Client(name, host, dict(port=int(port), colors=bool(colors))).main()

        # 
        elif args[0] == "hosting":
            # if you're using a provider
            # get port from envirment varibles
            port = int(os.environ.get("PORT") or 7777)
            # set host to 0.0.0.0 (all)
            host = "0.0.0.0"
            # print port you're using
            print(port)
            # and start server
            Server(port, dict(host=host)).main()

        # only one argument (run default settings)
        elif args[0] == "server":
            Server(7777).main()
        else:
            name = input("Type Username: ")
            Client(name, args[0]).main()

    # if you have two arguments you can specify a port for the server
    # and a port for the client as such:
    #
    # rewraa server $port
    # rewraa $hostname $port

    elif len(args) == 2:
        # check for server
        if args[0] == "server":
            Server(int(args[1])).main()
        else:
            name = input("Type Username: ")
            Client(name, args[0], dict(port=int(args[1]), colors=supports_color())).main()

    # with three arguments we have the option to specify the use of colors
    elif len(args) == 3:
        # full on stuff
        if args[0] == "server":
            Server(int(args[2]), dict(host=args[1])).main()
        else:
            name = input("Type Username: ")
            Client(name, args[0], dict(port=int(args[1]), colors=bool(args[2]))).main()
    elif len(args) == 4:
        # if the last one is the username
        Client(args[3], args[0], dict(port=int(args[1]), colors=bool(args[2]))).main()
    else:
        print("Not enough arguments (or to many. max 3)")
        exit()

# main stament for runnning
# as a command
if __name__ == "__main__":
    try:
        main()
    except Exception as Error:
        print(Error)
        pass
