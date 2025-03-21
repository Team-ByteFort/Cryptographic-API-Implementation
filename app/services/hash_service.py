import hashlib
import hmac

class HashService:
    @staticmethod
    def GenerateHash(data, algorithm):
        if algorithm == "SHA-256":
            return hashlib.sha256(data.encode()).hexdigest()
        elif algorithm == "SHA-512":
            return hashlib.sha512(data.encode()).hexdigest()
        else:
            raise ValueError("Unsupported hashing algorithm")

    @staticmethod
    def VerifyHash(data, hash_value, algorithm):
        computed_hash = HashService.GenerateHash(data, algorithm)
        return hmac.compare_digest(computed_hash, hash_value)


