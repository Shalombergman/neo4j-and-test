from flask import Blueprint, current_app, request, jsonify

from repositories.device_repository import DeviceRepository

phone_blueprint = Blueprint("phone", __name__, url_prefix="/api")



@phone_blueprint.route("/phone_tracker", methods=['POST'])
def create_phone_tracker():
    data = request.json
    DeviceRepository.create_interaction_with_interaction(data)
    return jsonify({"status": "success"}), 200


