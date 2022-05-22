"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

CCredentials Module: Low-level abstraction for encrypting credentials.

Manages credentials throuh symmetrical encryption using 
AES cipher and SHA256 for the random number generation and
hashing.

Classes
-------
CCredentials( path : str )

"""

import pickle
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

class CCredentials( object ):
    """
    CCredentials Module: Low-level abstraction for encrypting credentials.

    Manages credentials throuh symmetrical encryption using 
    AES cipher and SHA256 for the random number generation and
    hashing.
    
    Attributes
    ----------
    path : str
        Path for dumping/loading credentials file.

    Methods
    -------

    """
    def __init__(self, path : str):
        self.path = path

    def encrypt(self, key : bytes, source : bytes) -> bytes:
        """
        Symmetrical encryption using AES cipher and
        SHA256 hashing. Padding included.

        Parameters
        ----------
        key : bytes
            passphrase for encryption.
        source : bytes
            serialized object.
        
        Returns
        -------
        bytes
            Serialized, padded and encryted data.

        """
        
        bSize = AES.block_size
        key         = SHA256.new(key).digest()
        salt        = Random.new().read(bSize)
        encryptor   = AES.new(key, AES.MODE_CBC, salt)
        padding     = ( bSize - len(source) ) % bSize
        source      = source + bytes([padding]) * padding
        data        = salt + encryptor.encrypt(source)
        return data

    def decrypt(self, key : bytes, source : bytes) -> bytes:
        """
        Symmetrical decryption using AES cipher and
        SHA256 hashing. Padding included.

        Parameters
        ----------
        key : bytes
            passphrase for decryption.
        source : bytes
            serialized encrypted object.
        
        Returns
        -------
        bytes
            Serialized and decryted data.

        """
        bSize = AES.block_size
        key         = SHA256.new(key).digest()
        salt        = source[:bSize]
        decryptor   = AES.new(key, AES.MODE_CBC, salt)
        data        = decryptor.decrypt(source[bSize:])
        padding     = data[-1]
        return data[ :-padding ]

    def dump( self, key : bytes, obj ) -> None:
        """
        Dump encrypted object

        Parameters
        ----------
        key : bytes
            pasphrase for encryption.
        obj : Any
            object to serialize.
        """
        serial_obj  = pickle.dumps( obj )
        encrypt_obj = self.encrypt( key, serial_obj )
        with open( self.path, "wb" ) as f:
            f.write( encrypt_obj )

    def load( self, key : bytes ):
        """
        Load encrypted object

        Parameters
        ----------
        key : bytes
            pasphrase for decryption.
        
        Returns
        -------
        Any
            object decrypted.
        """
        with open( self.path, "rb" ) as f:
            encrypt_obj = f.read()
        serial_obj  = self.decrypt( key, encrypt_obj )
        try:
            obj     = pickle.loads( serial_obj )
        except pickle.UnpicklingError:
            obj     = {}
        return obj
