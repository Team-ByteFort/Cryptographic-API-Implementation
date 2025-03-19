from flask import Blueprint, request, jsonify
from app.services.encryption_service import EncryptionService
encrypt_routes = Blueprint('encrypt_routes', __name__)

@encrypt_routes.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    key_id = data.get("key_id")
    plaintext = data.get("plaintext")
    algorithm = data.get("algorithm")
    if algorithm == "AES" or algorithm == "RSA":
        ciphertext  = EncryptionService.encrypt(plaintext, key_id, algorithm)
    else:
        return jsonify({"error": "Unsupported algorithm. Use 'AES' or 'RSA'."}), 400
    
    return jsonify({"ciphertext": ciphertext})

@encrypt_routes.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    key_id = data.get("key_id")
    ciphertext = data.get("ciphertext")
    algorithm = data.get("algorithm")
    if algorithm == "AES" or algorithm == "RSA":
        plaintext = EncryptionService.decrypt(ciphertext, key_id, algorithm)
    else:
        return jsonify({"error": "Unsupported algorithm. Use 'AES' or 'RSA'."}), 400
    return jsonify({"plaintext": plaintext})