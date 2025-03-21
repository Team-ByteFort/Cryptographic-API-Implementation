import hashlib
import hmac


class HashService:
    @staticmethod
    def GenerateHash(data, algorithm):
        response = {"error": "An error occurred while processing the request."}  # Default response

        try:
            if algorithm == "SHA-256":
                hash_value = hashlib.sha256(data.encode()).hexdigest()
            elif algorithm == "SHA-512":
                hash_value = hashlib.sha512(data.encode()).hexdigest()
            else:
                raise ValueError("Unsupported hashing algorithm")

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
