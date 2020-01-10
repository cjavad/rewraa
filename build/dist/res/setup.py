import re
from setuptools import Extension
from setuptools import setup as setup_

LONG_DES = """
RewRaa (RSA ENCRYPTED WILD ROUND AES APPLICATION, note i have no idea why i choose that name)
is a socket-server chat program which uses rsa encryption to encrypt an aes key for encrypting/decrypting messages

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

NOTE: Only connect to trusted servers for now it has a big security flaw and the only secure part is if anyone is monitoring your internet traffic
"""

# get version
verstr = "unknown"
try:
    # from main.py
    verstrline = open('../dist/main.py', "rt").read()
except EnvironmentError:
    pass # Okay, there is no version file.
else:
    # use regex
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        # version string
        verstr = mo.group(1)
    else:
        # else stop and exit
        raise RuntimeError("unable to find version in main.py")

# setup

setup_(
    name="rewraa",
    author="Javad Shafique",
    author_email="javadscript@gmx.com",
    version=verstr,
    install_requires=["pycryptodome"],
    setup_requires=["cython"],
    ext_modules=[
        # build C code my best attempt to protect my sourcecode
        # good luck reading that. 
        Extension("rewraa", ["rewraa.c"])
    ],
    description="A Encrypted Chat program",
    long_description=LONG_DES,
    entry_points = {
        "console_scripts": [
            "rewraa = rewraa:main"
        ]
    },
    # Package data (icon, license)
    include_package_data=True
)