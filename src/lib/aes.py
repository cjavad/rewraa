import base64 # for encoding and decoding
import binascii # import for hex function
from Crypto.Cipher import AES # import for aes encryption
from Crypto import Random

"""
Here is a bunch of decoding/encoding functions for diffrent things
"""
# encode unicode to hex
def hex_encode(string):
    # and return ascii string
    return binascii.hexlify(str(string).encode("unicode_escape")).decode("ascii")

# decode ascii encoded hex string to unicode
def hex_decode(string):
    # convert to bytes
    string = string.encode()
    # decode hex and unicode
    return binascii.unhexlify(string).decode("unicode_escape")

# base64 encoding and decoding with unicode
def b64_encode(string):
    return base64.b64encode(str(string).encode("unicode_escape")).decode("ascii")

def b64_decode(string):
    # convert to bytes
    string = string.encode()
    return base64.b64decode(string).decode("unicode_escape")


# and the ones we a using
encode = b64_encode
decode = b64_decode

# aes encryption class. 
# used for encrypting data 
# have a encrypt and decrypt
# function.

"""
Aes encryption class
"""

class aes:
    # define error
    class InvalidBlockSizeError(Exception):
        """Raised for invalid block sizes"""
        pass

    # constuctor takes key
    def __init__(self, key):
        # pad key
        key = key.zfill(32)
        # convert key to bytes
        self.key = key[0:32].encode()
   
    # padding
    def __pad(self, text):
        amount_to_pad = AES.block_size - (len(text) % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    # remove padding
    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]

    # encrypt data
    def encrypt(self, data):
        # pad and convert to bytes
        raw = self.__pad(data).encode()
        # init cipher
        # but first create iv
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # return base64 encrypted bytes
        return base64.b64encode(iv + cipher.encrypt(raw))

    # decrypt
    def decrypt(self, enc):
        # decode encrypted string
        enc = base64.b64decode(enc)
        # init cipher
        # first extract iv
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # unpad the decrypted bytes that we convert to utf-8
        return self.__unpad((cipher.decrypt(enc[AES.block_size:]).decode("utf8")))

"""
e = encode("Javad NANE IS LOL")
print(e, decode(e))

||||||||||||||||||||||

msg = input("Message: ")
pwd = input("Password: ")
a = aes(pwd)
e = a.encrypt(msg)
d = a.decrypt(e)

print("Encrypted:", e)
print("Decrypted:", d)
"""