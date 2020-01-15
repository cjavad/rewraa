from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

class rsa:
    def __init__(self, bits = 4096, keys = None):
        if keys == None:
            self.keys = RSA.generate(bits, Random.new().read)
            self.pub = self.keys.publickey().exportKey()
            self.pem = self.keys.exportKey()
        else:
            self.keys = RSA.importKey(keys)
            self.pub = self.keys.publickey().exportKey()
            self.pem = self.keys.exportKey()

    def encrypt(self, data):
        return PKCS1_OAEP.new(self.keys.publickey()).encrypt(data.encode())

    def decrypt(self, encrypted):
        return PKCS1_OAEP.new(self.keys).decrypt(encrypted)

    #for encrypting with the public key only
    @staticmethod
    def _encrypt(data, public):
        return PKCS1_OAEP.new(RSA.importKey(public)).encrypt(data.encode())
