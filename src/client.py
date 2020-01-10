import socket
import threading
from os import _exit
"""
Importing one by one so our create.py can
use it without added namespaces ( classes )
"""
from lib.aes import aes, encode, decode
from lib.rsa import rsa
from lib.tools import write, read
from lib.colors import color

# Seprator for printing messages
# it's blank when you're using colors
# but when there is no colors it becomes
# a colon ":".

COLOR_SEP = ""

""" client class
Takes 3 (4) arguments:
 - str [name]; The username you want to use
 - str [host]; Ipaddress or host name of server
 - dict [options]; Dict with to arguments
    * int [port] The port to listen on default 7777
    * bool [colors] To use colors in terminal only use if your shell/terminal supports it
"""

class Client:
    # constuctor (initilizer) takes 3 (4) Arguments
    def __init__(self, name, host, options = {"port":7777, "colors":False}):
        # check colors
        if not options["colors"]:
            # if colors is off, override function
            # and set COLOR_SEP to colon
            global color, COLOR_SEP
            COLOR_SEP = ":"
            color = lambda msg, col: msg

        # generate rsa keypair
        self.keys = rsa()
        # set key varible to None
        self.key = None
        # set name to name
        self.name = name
        # create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # and connect to address
        self.sock.connect((host, options["port"]))

    """
    ClientGetMsg (client) takes some input, checks
    if it's a command and either executes the command 
    or returns the message 
    """

    def GetMsg(self):
        i =  input("")

        if i == "/exit":
            # exit with os._exit
            _exit(0)
        else:   
            return i
    """
    ClientSendMsg (client, msg) takes a single argument, the message
    which it formats and encrypt, so it can send it to
    the server
    """

    def SendMsg(self, msg):
        # check if message includes anything
        if len(msg) == 0:
            # Do nothing
            pass
        else:
            # Create message
            msg = self.name + ": " + msg
            # Encrypt message
            msg = aes(self.key).encrypt(encode(msg))
            # and write it to server
            write(msg, self.sock)
    """
    Client__thread (client) is a function that is 
    made to be runned in a seprate thread so it can
    read data from server in the background
    """

    def __thread(self):
        while True:
            # While true read incomming messages
            msg = read(self.sock)
            try:
                # and try to decode it as a normal
                # message.

                # By Decrypting it
                msg = decode(aes(self.key).decrypt(msg))
                # And formating it with colors
                if msg.split(" ").pop() == "Disconnected":
                    print(color(msg, "yellow"))
                else:
                    # And charecters
                    print(color(msg.split(":")[0] + COLOR_SEP, "blue") + " " + color(':'.join(msg.split(":")[1:]), "green"))
            # if and exception occurs
            except Exception as e:
                # decode message
                msg = msg.decode("utf8")
                # and print it
                print(color(msg, "red"))
    """
    Clientmain (client) is the main process that starts
    the Client__thread and waits for input to be send with
    ClientGetMsg and ClientSendMsg.
    """
    def main(self):
        try:
            # key exhange
            write(self.keys.pub, self.sock)
            self.key = self.keys.decrypt(read(self.sock)).decode("utf8")
            write(aes(self.key).encrypt(encode(self.name)), self.sock)
            # start thread
            threading.Thread(target=self.__thread).start()
            # and while True
            while True:
                # send messages
                self.SendMsg(self.GetMsg())
        
        except Exception as e:
            # if any error occurs
            # print it. it's probaly from
            # the self.__thread
            print(color(e, "red"))
