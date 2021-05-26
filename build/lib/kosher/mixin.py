#!/usr/bin/env python
# kosher.py - Provides mixin for encrypting pickles.
__version__ = '0.2'

import os
import ast #
import base64
import hashlib
import json
import pickle
import sys
import logging
from typing import types

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from Crypto.Cipher import AES
from Crypto import Random
#from Crypto.Random import get_random_bytes
#from Crypto.Hash import HMAC, SHA, SHA256, SHA384, SHA512

CIPHER = 'AES' # Default cipher if not set.
BLOCK_SIZE = AES.block_size
SALT_SIZE = 16
SHA = 'SHA256'
#SHA = 'SHA512'

# Are pickles kosher?
if 'DILL' in os.environ:
    MOT = os.environ['DILL']
else:
    MOT = 'supersecret'

offsets = {
    'aes': BLOCK_SIZE,
    'fernet': SALT_SIZE,
    }

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')
log = logging.getLogger(__name__).error


class KosherPickleMixin(object):
    """ Mixin for encrypting pickles. """

    def __getstate__(self):
        if 'MOT' in globals():

            return self.encrypt(self.__dict__, MOT, CIPHER) # CIPHER not needed here.
        else:

            return self.__dict__

    def __setstate__(self, obj):
        if isinstance(obj, bytes) and 'MOT' in globals():
            try:
                self.__dict__ = self.decrypt(obj, MOT, CIPHER) # CIPHER not needed here.
            except Exception as e:
                log(e)
        elif isinstance(obj, bytes) and 'MOT' not in globals():
            log("Encrypted file requires authentication.")
        elif not isinstance(obj, bytes) and 'MOT' in globals():
            log("You have a password set but the file is not encrypted. Is that correct?")
        else:
            return obj.__dict__

    def keys(self, cipher, *args, **kwargs):
        try:
            key_gen = getattr(self, cipher.lower() + '_key')
            key = key_gen(*args, **kwargs)
        except Exception as e:
            log(e)

        return key

    def aes_key(self, mot, *args, **kwargs): #
        """ This is really just a password hash. """
        return hashlib.sha256(mot.encode("utf-8")).digest(), b'' # Unsalted.

    def fernet_key(self, mot, salt=None, sha=SHA):
        if salt is None:
            salt = os.urandom(SALT_SIZE)
        mot = mot.encode()
        kdf = PBKDF2HMAC(
            algorithm = getattr(hashes, sha),
            length = 32,
            salt = salt,
            iterations = 100_000,
            backend = default_backend(),
            )

        return base64.urlsafe_b64encode(kdf.derive(mot)), salt

    # This should be a registry, not a parser.
    def scheme(self, cipher, key, iv=None):
        """ Refactor here to accomodate AES having extra nestng layer.  """
        if cipher.lower() == 'aes':
        #if self._algo  in globals() and isinstance(globals()[self._algo], types.ClassType):
            try:
                clef = [key]
                params = self.algos[cipher]
                if iv is None:
                    iv = params['iv']
                else:
                    params['iv'] = iv
                for x in list(params.values()):
                    clef.append(x)
                params = tuple(clef)

            except Exception as e:
                log(e)

            return AES.new(*params), iv

        #if self._algo in globals():
        if cipher.lower() == 'fernet':
            #return globals()[self.algo](key), b'' # Who thought this was a good idea.
            return globals()[cipher](key), b'' # Who thought this was a good idea.

    def encrypt(self, data, mot, cipher=CIPHER):
        protocol=None
        fix_imports=True

        try:
            key, salt = self.keys(cipher, mot)
            cipher, iv = self.scheme(cipher, key)
            pickled = pickle.dumps(
                data,
                protocol=protocol,
                fix_imports=fix_imports
                )
            encrypted = iv + cipher.encrypt(pickled)

        except Exception as e:
            log(e)

        return salt + encrypted

    def decrypt(self, data, mot, cipher=CIPHER):
        fix_imports=True
        encoding="ASCII"
        errors="strict"

        try:
            offset_size = offsets[cipher.lower()]
            offset = data[:offset_size]
            key, salt = self.keys(cipher, mot, offset)
            decipher, iv = self.scheme(cipher, key, offset)
            encrypted_data = data[offset_size:]
            deciphered = decipher.decrypt(encrypted_data)

        except Exception as e:
            print(e)

        return pickle.loads(
            deciphered,
            fix_imports=fix_imports,
            #encoding=encoding,
            #errors=errors
            )

    @property
    def algo(self):
        """ Return env cipher if cipher not set. """
        return CIPHER

    """
    @algo.setter
    def algo(self, algor: str):
        if algor in self.algos:
            self._algo = algor
        else:
            print("Sorry, " + algor + " is not currently supported.")
    """

    @property
    def algos(self):
        """ Encryption algorithm parameters kwargs """
        self._algos = {
            'AES': {'mode': AES.MODE_CFB, 'iv': self.aes_iv()},
            'Fernet': {''},
            }

        return self._algos

    def aes_iv(self):
        iv = Random.new().read(AES.block_size)
        # iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
        return iv

    def _pad(self, s):
        bs = AES.block_size
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs) # Equivalent

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def derive_key(self, pw, salt, sha=SHA):
        pw = pw.encode()
        kdf = PBKDF2HMAC(
            algorithm = getattr(hashes, sha),
            length = 32,
            salt = salt,
            iterations = 100_000,
            backend = default_backend(),
            )

        return base64.urlsafe_b64encode(kdf.derive(pw))
