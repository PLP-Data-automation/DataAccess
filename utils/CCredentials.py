import pickle
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

class CCredentials( object ):
    def __init__(self, path):
        self.path = path

    def encrypt(self, key, source):
        bSize = AES.block_size
        key         = SHA256.new(key).digest()
        salt        = Random.new().read(bSize)
        encryptor   = AES.new(key, AES.MODE_CBC, salt)
        padding     = ( bSize - len(source) ) % bSize
        source      = source + bytes([padding]) * padding
        data        = salt + encryptor.encrypt(source)
        return data

    def decrypt(self, key, source):
        bSize = AES.block_size
        key         = SHA256.new(key).digest()
        salt        = source[:bSize]
        decryptor   = AES.new(key, AES.MODE_CBC, salt)
        data        = decryptor.decrypt(source[bSize:])
        padding     = data[-1]
        return data[ :-padding ]

    def dump( self, key, obj ):
        serial_obj  = pickle.dumps( obj )
        encrypt_obj = self.encrypt( key, serial_obj )
        with open( self.path, "wb" ) as f:
            f.write( encrypt_obj )

    def load( self, key ):
        with open( self.path, "rb" ) as f:
            encrypt_obj = f.read()
        serial_obj  = self.decrypt( key, encrypt_obj )
        try:
            obj     = pickle.loads( serial_obj )
        except pickle.UnpicklingError:
            obj     = {}
        return obj
