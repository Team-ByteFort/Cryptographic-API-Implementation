import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)

from app.services.key_service import KeyService


class EncryptionService:
    @staticmethod
    def encrypt(plaintext, key_id, algorithm):
        response = {"error": "An error occurred while processing the request."}  # Default response

        try:
            key_entry = KeyService.get_key_by_id(key_id)

            if not key_entry:
                return {"error": "Invalid key_id. Key not found."}, 400

            key_type = key_entry["key_type"]

            if key_type == "AES" and algorithm == "AES":
                key_value = base64.b64decode(key_entry["key_value"])
                iv = os.urandom(16)  # Generate a random IV for each encryption
                cipher = Cipher(algorithms.AES(key_value), modes.CBC(iv), backend=default_backend())
                encryptor = cipher.encryptor()

                # Pad plaintext to be a multiple of block size
                pad_length = 16 - (len(plaintext) % 16)
                padded_plaintext = plaintext + chr(pad_length) * pad_length

                ciphertext = encryptor.update(padded_plaintext.encode()) + encryptor.finalize()

                # Include the IV in the final output
                response = base64.b64encode(iv + ciphertext).decode()
                response = {"ciphertext": response}
                return response

            elif key_type == "RSA" and algorithm == "RSA":
                public_key = base64.b64decode(key_entry["public_key"])  # Get public key
                public_key = load_pem_public_key(public_key, backend=default_backend())

                ciphertext = public_key.encrypt(
                    plaintext.encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None,
                    ),
                )

                response = base64.b64encode(ciphertext).decode()  # Return encoded ciphertext
                response = {"ciphertext": response}
                return response

            else:
                return {"error": "Invalid key_type or algorithm."}, 400

        except Exception as e:
            return {"error": f"Encryption failed: {str(e)}"}, 500

    @staticmethod
    def decrypt(ciphertext, key_id, algorithm):
        response = {"error": "An error occurred while processing the request."}  # Default response

        try:
            key_entry = KeyService.get_key_by_id(key_id)

            if not key_entry:
                return {"error": "Invalid key_id. Key not found."}, 400

            key_type = key_entry["key_type"]

            # Ensure correct AES key size
            if key_type == "AES" and algorithm == "AES":
                key_value = base64.b64decode(key_entry["key_value"])
                if len(key_value) not in [16, 24, 32]:
                    return {"error": "Invalid key size for AES encryption."}, 400

                data = base64.b64decode(ciphertext)

                if len(data) < 16:
                    return {"error": "Ciphertext is too short."}, 400

                iv, ciphertext = data[:16], data[16:]  # Extract IV and actual ciphertext

                cipher = Cipher(algorithms.AES(key_value), modes.CBC(iv), backend=default_backend())
                decryptor = cipher.decryptor()
                decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

                result = EncryptionService.unpad(decrypted_padded)
                if isinstance(result, dict):  # Check if unpad returned an error
                    return result

                response = result.decode()
                return response

            elif key_type == "RSA" and algorithm == "RSA":
                private_key = base64.b64decode(key_entry["private_key"])  # Get private key
                private_key = load_pem_private_key(
                    private_key, password=None, backend=default_backend()
                )

                decrypted = private_key.decrypt(
                    base64.b64decode(ciphertext),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None,
                    ),
                )

                response = decrypted.decode()
                return response

            else:
                return {"error": "Invalid key_type or algorithm."}, 400

        except Exception as e:
            return {"error": f"Decryption failed: {str(e)}"}, 500

    @staticmethod
    def pad(data):
        padding_length = 16 - (len(data) % 16)
        return data + bytes([padding_length] * padding_length)

    @staticmethod
    def unpad(data):
        if not data:  # Check for empty data
            return {"error": "Decryption failed, empty result"}, 400

        padding_length = data[-1]

        if padding_length > 16 or padding_length > len(data):  # Prevent invalid padding
            return {"error": "Invalid padding detected"}, 400

        return data[:-padding_length]
