from flask import Blueprint, request, jsonify
from app.services.hash_service import HashService


hash_routes = Blueprint('hash_routes', __name__)

@hash_routes.route('/generate-hash', methods=['POST'])
def generate_hash():
    data = request.json
    message = data.get('data')
    algorithm = data.get('algorithm')
    if algorithm == "SHA-256" or algorithm == "SHA-512":
        hash_value = HashService.GenerateHash(message, algorithm)
    else:
        return jsonify({"error": "Unsupported algorithm. Use 'SHA-256' or 'SHA-512'."}), 400
    return jsonify({"hash_value": hash_value, "algorithm": algorithm})

@hash_routes.route('/verify-hash', methods=['POST'])
def verify_hash():
    data = request.json
    message = data.get('data')
    hash_value = data.get('hash_value')
    algorithm = data.get('algorithm')
    if algorithm == "SHA-256" or algorithm == "SHA-512":
        is_valid = HashService.VerifyHash(message, hash_value, algorithm)
    else:
        return jsonify({"error": "Unsupported algorithm. Use 'SHA-256' or 'SHA-512'."}), 400
    
    if is_valid:
        return_message = "Hash matches the data."
    else:
        return_message = "Hash does not match the data."
    return jsonify({"is_valid": is_valid, "message": return_message})
