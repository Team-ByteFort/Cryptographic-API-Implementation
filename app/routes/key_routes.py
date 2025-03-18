from flask import Blueprint, request, jsonify

key_routes = Blueprint('key_routes', __name__)

@key_routes.route('/generate-key', methods=['POST'])
def generate_key():
    data = request.json
    key_type = data.get("key_type")
    key_size = data.get("key_size")

    return jsonify({"message": f"Key generation for {key_type} with size {key_size} will be implemented."})
