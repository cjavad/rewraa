import re
from setuptools import Extension, find_packages
from setuptools import setup as setup_

LONG_DES = """
RewRaa (RSA ENCRYPTED WILD ROUND AES APPLICATION, note i have no idea
why i choose that name) is a socket-server chat program which uses rsa
encryption to encrypt an aes key for encrypting/decrypting messages

Imagine the following encryption scheme:

::

    # first transfer aes key
    (CLIENT) => RSA_PUBLIC => (SERVER)
    (SERVER) => RSA_ENCRYPTED_AES_KEY => (CLIENT)

            (C) => ENC_DATA => (S)
                        - BROADCAST -
                        (C) - (C) - (C) # clients decrypt the message

But working to give each client a seprate aes-key and signing the data
so you can’t create a fake server that reads all your data.

NOTE: Only connect to trusted servers for now it has a big security flaw
and the only secure part is if anyone is monitoring your internet
traffic
"""

# get version
verstr = "unknown"

try:
    # from main.py
    verstrline = open('../main.py', "rt", encoding="utf-8").read()
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
name = "rewraa"
author="Javad Shafique"
author_email="javadscript@gmx.com"
install_requires=["pycryptodome"]
description="A Encrypted Chat program"
entry_points = {
    "console_scripts": [
        "rewraa = rewraa:main"
    ]
}
include_package_data=True

# disable c compiling for now

if False:
    setup_(
        name=name,
        author=author,
        author_email=author_email,
        version=verstr,
        install_requires=install_requires,
        setup_requires=["cython"],
        ext_modules=[
            # build C code my best attempt to protect my sourcecode
            # good luck reading that. 
            Extension("rewraa", ["rewraa.c"])
        ],
        description=description,
        long_description=LONG_DES,
        entry_points=entry_points,
        # Package data (icon, license)
        include_package_data=include_package_data
    )
# Only build if possible
else:
    setup_(
        name=name,
        author=author,
        author_email=author_email,
        version=verstr,
        install_requires=install_requires,
        packages=find_packages(),
        description=description,
        long_description=LONG_DES,
        entry_points=entry_points,
        # Package data (icon, license)
        include_package_data=include_package_data
    )