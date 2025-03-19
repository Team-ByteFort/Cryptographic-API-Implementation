import os
import base64
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend

# In-memory key storage
KEY_STORAGE = {}

class KeyService:
    @staticmethod
    def generate_aes_key(key_size=256):
        key = os.urandom(key_size // 8)  # Generate a random key of key_size bits and convert to bytes
        
        key_id = str(uuid.uuid4())  # Generate a unique key ID
        key_value = base64.b64encode(key).decode()
        
        # Store key for future use
        KEY_STORAGE[key_id] = {"key_type": "AES", "key_value": key_value}
        return key_id, key_value

    @staticmethod
    def generate_rsa_key():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        private_pem = private_key.private_bytes(
            Encoding.PEM,
            PrivateFormat.PKCS8,
            NoEncryption()
        )

        key_value = base64.b64encode(private_pem).decode()

        key_id = str(uuid.uuid4())

        # Store key for future use
        KEY_STORAGE[key_id] = {"key_type": "RSA", "key_value": key_value}
        return key_id, key_value

    @staticmethod
    def get_key_by_id(key_id):
        return KEY_STORAGE.get(key_id)


