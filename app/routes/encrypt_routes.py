from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.models.dto import DecryptionRequest, EncryptionRequest
from app.services.encryption_service import EncryptionService

encrypt_routes = Blueprint("encrypt_routes", __name__)


@encrypt_routes.route("/encrypt", methods=["POST"])
def encrypt():
    response = {"error": "An error occurred while processing the request."}  # Default response
    try:
        # Parse JSON request data and validate it with the Pydantic model
        data = request.get_json()
        encryption_request = EncryptionRequest(**data)
        encryption_request = encryption_request.model_dump()

        # If validation passes, proceed with the data
        key_id = encryption_request.get("key_id")
        plaintext = encryption_request.get("plaintext")
        algorithm = encryption_request.get("algorithm")

        if algorithm == "AES" or algorithm == "RSA":
            response = EncryptionService.encrypt(plaintext, key_id, algorithm)
        else:
            return jsonify({"error": "Unsupported algorithm. Use 'AES' or 'RSA'."}), 400

        return response

    except ValidationError as e:
        # If validation fails, return the error details
        return jsonify(e.errors()), 400


@encrypt_routes.route("/decrypt", methods=["POST"])
def decrypt():
    response = {"error": "An error occurred while processing the request."}  # Default response
    try:
        # Parse JSON request data and validate it with the Pydantic model
        data = request.get_json()
        decryption_request = DecryptionRequest(**data)
        decryption_request = decryption_request.model_dump()

        # If validation passes, proceed with the data
        key_id = decryption_request.get("key_id")
        ciphertext = decryption_request.get("ciphertext")
        algorithm = decryption_request.get("algorithm")

        if algorithm == "AES" or algorithm == "RSA":
            response = EncryptionService.decrypt(ciphertext, key_id, algorithm)
        else:
            return jsonify({"error": "Unsupported algorithm. Use 'AES' or 'RSA'."}), 400
        return response

    except ValidationError as e:
        # If validation fails, return the error details
        return jsonify(e.errors()), 400
