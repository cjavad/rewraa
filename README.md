### Background

I made this early 2017 so it's pretty far off what i would call "recent", but looking at some old decently 
commented coded was pretty fun so i decided to just clean up a bit, no changing any code, just checking if
the system i sat up back then still works now. And surprise it does, and very well infact so i've decided to
just put it up for the memes and watch how my make-file rip off and self coded argparser holds up.

On a side note tests/ is a weird place i fucked around in back in the day but for old time sake i've kept it in here.

# Rewraa

```
██████╗ ███████╗██╗    ██╗██████╗  █████╗  █████╗ 
██╔══██╗██╔════╝██║    ██║██╔══██╗██╔══██╗██╔══██╗
██████╔╝█████╗  ██║ █╗ ██║██████╔╝███████║███████║
██╔══██╗██╔══╝  ██║███╗██║██╔══██╗██╔══██║██╔══██║
██║  ██║███████╗╚███╔███╔╝██║  ██║██║  ██║██║  ██║
╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
                                                  
```

RewRaa (RSA ENCRYPTED WORLD RELIC AES APPLICATION, note i have no idea why i choose that name)
is a socket-server chat program which uses rsa encryption to encrypt an aes key for encrypting/decrypting messages.

Imagine the following encryption scheme:
```
# first transfer aes key
(CLIENT) => RSA_PUBLIC => (SERVER)
(SERVER) => RSA_ENCRYPTED_AES_KEY => (CLIENT)

        (C) => ENC_DATA => (S)
                    - BROADCAST -
                    (C) - (C) - (C) # clients decrypt the message

```

But working to give each client a seprate aes-key and signing the data so you can't create a fake server
that reads all your data. 

# Building

To install Rewraa you can run the build files in ./build (build.sh for macos/linux and build.cmd for windows)
rewraa requires the pypi packages found in requirements.txt to build.

The format is `build.* [mode]` where [mode] is one of the following:

        clean
        create
        build

Also run in that order. See build/README.md for more information.

# Installing

After building Rewraa you can simply install it by running `python3 setup.py install`
and the command rewraa is now installed on your system.

# Usage

For server: 
   rewraa server port (host, port)
For client: 
   rewraa host, port useColors? username

This program can run in five modes: 

        Mode 1: Setup, here it's all interactive. No arguments

        Mode 2: Quick, if you pass one argument either 'server' or the hostname of the computer you want to connect to

        Mode 3: Custom, The first argument is the same as in Quick but now you can pass a port as the second argument

        Mode 4: Full, Same as custom but the arguments for server is passed like this ('server', host, port) and the client (host, port, useColors?)

        Mode 5: Quiet, This mode is the same as full but takes one last argument the username for the client so as this (host, port, useColors?, name)

Some other modes comming up:
 
rewraa hosting: starts a server with the PORT environ variable
rewraa filename.rewraa: reads file as json and tries to get port, host, and username from it

        Use --help (/help, /?) to get this message
        Use --version (-v) to get the version of this program
        Use --license (/license) to get the license
        Use --author for the note left by the author


NOTE: All modes using client that isn't Quiet ask for a username. Mode 2 with server listens on port 7777, the server does not take input
