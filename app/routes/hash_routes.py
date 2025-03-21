from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.models.dto import HashRequest, HashVerificationRequest
from app.services.hash_service import HashService

hash_routes = Blueprint("hash_routes", __name__)


@hash_routes.route("/generate-hash", methods=["POST"])
def generate_hash():
    response = {"error": "An error occurred while processing the request."}  # Default response
    try:
        # Parse JSON request data and validate it with the Pydantic model
        data = request.get_json()
        hash_request = HashRequest(**data)
        hash_request = hash_request.model_dump()

        # If validation passes, proceed with the data
        message = hash_request.get("data")
        algorithm = hash_request.get("algorithm")

        if algorithm == "SHA-256" or algorithm == "SHA-512":
            response = HashService.GenerateHash(message, algorithm)
        else:
            return jsonify({"error": "Unsupported algorithm. Use 'SHA-256' or 'SHA-512'."}), 400
        return response

    except ValidationError as e:
        # If validation fails, return the error details
        return jsonify(e.errors()), 400


@hash_routes.route("/verify-hash", methods=["POST"])
def verify_hash():
    response = {"error": "An error occurred while processing the request."}  # Default response
    try:
        # Parse JSON request data and validate it with the Pydantic model
        data = request.get_json()
        hash_verification_request = HashVerificationRequest(**data)
        hash_verification_request = hash_verification_request.model_dump()

        # If validation passes, proceed with the data
        message = hash_verification_request.get("data")
        hash_value = hash_verification_request.get("hash_value")
        algorithm = hash_verification_request.get("algorithm")

        if algorithm == "SHA-256" or algorithm == "SHA-512":
            response = HashService.VerifyHash(message, hash_value, algorithm)
        else:
            return jsonify({"error": "Unsupported algorithm. Use 'SHA-256' or 'SHA-512'."}), 400
        return response

    except ValidationError as e:
        # If validation fails, return the error details
        return jsonify(e.errors()), 400
