from flask import Blueprint, jsonify, request

from app.services.key_service import KeyService

key_routes = Blueprint("key_routes", __name__)


@key_routes.route("/generate-key", methods=["POST"])
def generate_key():
    data = request.json
    key_type = data.get("key_type")
    key_size = data.get("key_size", 256)  # Default to 256-bit for AES

    if key_type == "AES":
        key_id, key_value = KeyService.generate_aes_key(key_size)
    elif key_type == "RSA":
        key_id, key_value = KeyService.generate_rsa_key(key_size)
    else:
        return jsonify({"error": "Unsupported key type. Use 'AES' or 'RSA'."}), 400

    return jsonify({"key_id": key_id, "key_value": key_value})
