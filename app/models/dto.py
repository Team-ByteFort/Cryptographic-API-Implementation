from pydantic import BaseModel

# Key Generation DTO
class KeyGenerationRequest(BaseModel):
    key_type: str
    key_size: int

class KeyGenerationResponse(BaseModel):
    key_id: str
    key_value: str

# Encryption DTO
class EncryptionRequest(BaseModel):
    key_id: str
    plaintext: str
    algorithm: str

class EncryptionResponse(BaseModel):
    ciphertext: str

# Decryption DTO
class DecryptionRequest(BaseModel):
    key_id: str
    ciphertext: str
    algorithm: str

class DecryptionResponse(BaseModel):
    plaintext: str

# Hashing DTO
class HashRequest(BaseModel):
    data: str
    algorithm: str

class HashResponse(BaseModel):
    hash_value: str
    algorithm: str

# Hash Verification DTO
class HashVerificationRequest(BaseModel):
    data: str
    hash_value: str
    algorithm: str

class HashVerificationResponse(BaseModel):
    is_valid: bool
    message: str
