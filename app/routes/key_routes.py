from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.models.dto import KeyGenerationRequest
from app.services.key_service import KeyService

key_routes = Blueprint("key_routes", __name__)


@key_routes.route("/generate-key", methods=["POST"])
def generate_key():
    response = {"error": "An error occurred while processing the request."}  # Default response
    try:
        # Parse JSON request data and validate it with the Pydantic model
        data = request.get_json()
        key_generation_request = KeyGenerationRequest(**data)
        key_generation_request = key_generation_request.model_dump()

        # If validation passes, proceed with the data
        key_type = key_generation_request.get("key_type")
        key_size = key_generation_request.get("key_size", 256)  # Default to 256-bit for AES

        if key_type == "AES":
            response = KeyService.generate_aes_key(key_size)
        elif key_type == "RSA":
            response = KeyService.generate_rsa_key(key_size)
        else:
            return jsonify({"error": "Unsupported key type. Use 'AES' or 'RSA'."}), 400

        return response

    except ValidationError as e:
        # If validation fails, return the error details
        return jsonify(e.errors()), 400
