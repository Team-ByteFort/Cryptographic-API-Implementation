import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from app.services.key_service import KeyService

class EncryptionService:
    @staticmethod
    def encrypt(plaintext, key_id, algorithm):
        key_entry = KeyService.get_key_by_id(key_id)
        
        if not key_entry:
            return {"error": "Invalid key_id. Key not found."}, 400
        
        key_type = key_entry["key_type"]
        
        key_value = base64.b64decode(key_entry["key_value"])
        
        

        if key_type == "AES" and algorithm == "AES":
            iv = os.urandom(16)  # Generate a random IV for each encryption
            cipher = Cipher(algorithms.AES(key_value), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()

            # Pad plaintext to be a multiple of block size
            pad_length = 16 - (len(plaintext) % 16)
            padded_plaintext = plaintext + chr(pad_length) * pad_length

            ciphertext = encryptor.update(padded_plaintext.encode()) + encryptor.finalize()

            # Include the IV in the final output
            return base64.b64encode(iv + ciphertext).decode()
        
        elif key_type == "RSA" and algorithm == "RSA":
            pass

        else:
            return {"error": "Invalid key_type or algorithm."}, 400

    @staticmethod
    def decrypt(ciphertext, key_id, algorithm):
        key_entry = KeyService.get_key_by_id(key_id)

        if not key_entry:
            return {"error": "Invalid key_id. Key not found."}, 400
        
        key_type = key_entry["key_type"]
        key_value = base64.b64decode(key_entry["key_value"])

        # Ensure correct AES key size
        if key_type == "AES" and algorithm == "AES":
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
            
            return result.decode()
    
        elif key_type == "RSA" and algorithm == "RSA":
            pass

        else:
            return {"error": "Invalid key_type or algorithm."}, 400

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


