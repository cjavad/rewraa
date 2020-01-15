import random
import socket
import string
import threading
from lib.rsa import rsa
from lib.aes import aes, encode, decode
from lib.tools import write, read

"""
Generates and random string of charecters [a-Z] and numbers [0-9]
that is Cryptograficly secure using SystemRandom()
"""

def generate(n = 32):
    return ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits) for x in range(n)])

"""server class
Takes 2 (3) Arguments:
 - int [port] the port to listen on
 - dict [options] dict with options
  * str [host] if you want to listen to an alternative host default "0.0.0.0"
"""
class Server:
    def __init__(self, port, options={"host":"0.0.0.0"}):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((options["host"], port))
        self.aeskey = generate()
        self.clients = set()
        self.clients_lock = threading.Lock()
    """
    Server.broadcast (server, data, _from) takes two arguments
    data the data to broadcast and _from which is the sender who
    not to send the message to. Uses a set and threading.Lock to 
    manage connected users.
    """
    def broadcast(self, data, _from):
        # broadcast to all users
        # with threading.Lock
        with self.clients_lock:
            # run over clients
            for client in self.clients:
                # if it's the sender
                if client == _from:
                    # if the client in the list is the
                    # broadcaster of the message, skip it.
                    pass
                # else
                else:
                    # send data over socket
                    write(data, client)
    """
    Server.__read (server, client) where client is
    the socket object to read from. it basicly broadcasts
    all data from the Client
    """
    def __read(self, client):
        # try to
        try:
            # while true to:
            while True:
                # read all messages
                msg = read(client)
                # and broadcast them
                self.broadcast(msg, client)
        # except for when a exception occurs
        except BrokenPipeError:
            # then end it
            # User disconnected
            return
    """
    Server.__thread (server, client) is the function
    which handles the Client it's meant to be runned
    in a seprate thread.
    """
    def __thread(self, client):
        # add client to client list 
        # with threading.Lock
        with self.clients_lock:
            self.clients.add(client)

        # exhange keys here
        # first read the public rsa key
        pub = read(client)
        # then encrypt the aes key with the public key
        key = rsa._encrypt(self.aeskey, pub)
        # then write the encrypted key
        write(key, client)
        # and read the aes encrypted username of the client
        name = decode(aes(self.aeskey).decrypt(read(client)))
        # main procress
        try:
            # send callback message
             # write ready message and start listening
             # this one is doing to be red
            write("READY...\nType /exit to exit \n\n", client)
            # start reading function
            self.__read(client)

        except BrokenPipeError:
            # then the user disconnected
            pass

        finally:
            # broadcast that the user is disconnecting
            # but encrypt it so no one can see the username
            encrypted_return = aes(self.aeskey).encrypt(encode(name + " Disconnected"))
            # broadcast and then
            self.broadcast(encrypted_return, client)
            # finally end the connection
            with self.clients_lock:
                # remove from senders set
                self.clients.remove(client)
            # and close the connection
            client.close()
    """
    Server.main (server) is the servers main process
    which listens and accepts connctions that it handles
    with Server.__thread which it starts in a new thread
    """
    def main(self):
        # while true
        while True:
            try:
                # start listening listen again each time
                self.sock.listen(1)
                # wait for connection
                client, conn = self.sock.accept()
                # when a client has connected start in a new thread
                threading.Thread(target=self.__thread, args=(client,)).start()
            except Exception as error:
                # print error probaly from thread
                print(error)
