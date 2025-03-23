import hmac

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class HashService:
    @staticmethod
    def GenerateHash(data, algorithm):
        response = {"error": "An error occurred while processing the request."}  # Default response

        try:
            if algorithm == "SHA-256":
                digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
            elif algorithm == "SHA-512":
                digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
            else:
                raise ValueError("Unsupported hashing algorithm")

            digest.update(data.encode())
            hash_value = digest.finalize().hex()

            response = {"hash_value": hash_value, "algorithm": algorithm}
        except Exception as e:
            response = {"error": str(e)}

        return response

    @staticmethod
    def VerifyHash(data, hash_value, algorithm):
        response = {"error": "An error occurred while processing the request."}

        computed_hash = HashService.GenerateHash(data, algorithm)
        is_valid = hmac.compare_digest(computed_hash["hash_value"], hash_value)

        if is_valid:
            response = {"is_valid": is_valid, "message": "Hash matches the data."}
        else:
            response = {"is_valid": is_valid, "message": "Hash does not match the data."}

        return response
