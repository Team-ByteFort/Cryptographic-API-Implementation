import base64
import os
import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

# In-memory key storage
KEY_STORAGE = {}


class KeyService:
    @staticmethod
    def generate_aes_key(key_size=256):
        response = {"error": "An error occurred while processing the request."}  # Default response

        try:
            key = os.urandom(
                key_size // 8
            )  # Generate a random key of key_size bits and convert to bytes

            key_id = str(uuid.uuid4())  # Generate a unique key ID
            key_value = base64.b64encode(key).decode()

            # Store key for future use
            KEY_STORAGE[key_id] = {"key_type": "AES", "key_value": key_value}

            response = {"key_id": key_id, "key_value": key_value}
        except Exception as e:
            response = {"error": f"An error occurred: {str(e)}"}

        return response

    @staticmethod
    def generate_rsa_key(key_size=2048):
        response = {"error": "An error occurred while processing the request."}  # Default response

        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537, key_size=key_size, backend=default_backend()
            )

            # Serialize Private Key
            private_pem = private_key.private_bytes(
                Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
            )

            # Serialize Public Key
            public_pem = private_key.public_key().public_bytes(
                Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
            )

            key_id = str(uuid.uuid4())

            # Store both keys
            KEY_STORAGE[key_id] = {
                "key_type": "RSA",
                "private_key": base64.b64encode(private_pem).decode(),
                "public_key": base64.b64encode(public_pem).decode(),
            }
            response = {"key_id": key_id, "public_key": base64.b64encode(public_pem).decode()}
        except Exception as e:
            response = {"error": f"An error occurred: {str(e)}"}
        return response

    @staticmethod
    def get_key_by_id(key_id):
        return KEY_STORAGE.get(key_id)
