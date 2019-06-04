from django.conf import settings

import base64
import binascii
import nacl.pwhash
import nacl.secret
import nacl.utils

class Encryption:
    def __init__(self, password):
        password = str(password).encode('UTF-8')
        kdf = nacl.pwhash.argon2i.kdf # our key derivation function
        salt = settings.SECRET_SALT
        key = kdf(nacl.secret.SecretBox.KEY_SIZE, password, salt)
        self.box = nacl.secret.SecretBox(key)
    def encode(self, secret_message):
        encrypted = self.box.encrypt(str(secret_message).encode('UTF-8'))
        encrypted_ascii = base64.b64encode(encrypted).decode("ascii")
        if '+' in encrypted_ascii:
            return self.encode(secret_message)
        return encrypted_ascii
    def decode(self, encrypted_message):
        try:
            return self.box.decrypt(base64.b64decode(encrypted_message, '-_')).decode('UTF-8')
        except binascii.Error:
            return self.box.decrypt(base64.b64decode(encrypted_message)).decode('UTF-8')
