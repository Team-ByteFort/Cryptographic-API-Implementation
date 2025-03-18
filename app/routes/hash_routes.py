from flask import Blueprint, request, jsonify

hash_routes = Blueprint('hash_routes', __name__)

@hash_routes.route('/generate-hash', methods=['POST'])
def generate_hash():
    data = request.json
    return jsonify({"message": "Hashing function will be implemented."})

@hash_routes.route('/verify-hash', methods=['POST'])
def verify_hash():
    data = request.json
    return jsonify({"message": "Hash verification will be implemented."})
