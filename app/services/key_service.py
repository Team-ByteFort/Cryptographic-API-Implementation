import base64
import os
import sqlite3
import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

# SQLite database setup for key storage

DB_PATH = "key_storage.db"


# Initialize the database
def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS keys (
            key_id TEXT PRIMARY KEY,
            key_type TEXT NOT NULL,
            key_value TEXT,
            private_key TEXT,
            public_key TEXT
        )
        """
    )
    conn.commit()
    conn.close()


initialize_database()


class KeyService:
    @staticmethod
    def generate_aes_key(key_size=256):
        response = {"error": "An error occurred while processing the request."}  # Default response

        # Validate AES key size
        if key_size not in (128, 192, 256):
            response = {"error": "Invalid AES key size. Must be 128, 192, or 256 bits."}
            return response

        try:
            key = os.urandom(
                key_size // 8
            )  # Generate a random key of key_size bits and convert to bytes

            key_id = str(uuid.uuid4())  # Generate a unique key ID
            key_value = base64.b64encode(key).decode()

            # Store key in the SQLite database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO keys (key_id, key_type, key_value, private_key, public_key)
                VALUES (?, ?, ?, ?, ?)
                """,
                (key_id, "AES", key_value, None, None),
            )
            conn.commit()

            # Retrieve the key from the database to ensure it was stored correctly
            cursor.execute("SELECT key_id, key_value FROM keys WHERE key_id = ?", (key_id,))
            row = cursor.fetchone()
            if row:
                response = {"key_id": row[0], "key_value": row[1]}
            else:
                response = {"error": "Key not found in the database."}
            conn.close()
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

            # Store both keys in the SQLite database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO keys (key_id, key_type, key_value, private_key, public_key)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    key_id,
                    "RSA",
                    None,
                    base64.b64encode(private_pem).decode(),
                    base64.b64encode(public_pem).decode(),
                ),
            )
            conn.commit()

            # Retrieve the public key from the database to ensure it was stored correctly
            cursor = conn.cursor()
            cursor.execute("SELECT key_id, public_key FROM keys WHERE key_id = ?", (key_id,))
            row = cursor.fetchone()
            if row:
                response = {"key_id": row[0], "public_key": row[1]}
            else:
                response = {"error": "Key not found in the database."}
            conn.close()
        except Exception as e:
            response = {"error": f"An error occurred: {str(e)}"}
        return response

    @staticmethod
    def get_key_by_id(key_id):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM keys WHERE key_id = ?", (key_id,))
            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    "key_id": row[0],
                    "key_type": row[1],
                    "key_value": row[2],
                    "private_key": row[3],
                    "public_key": row[4],
                }
            else:
                return {"error": "Key not found."}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
