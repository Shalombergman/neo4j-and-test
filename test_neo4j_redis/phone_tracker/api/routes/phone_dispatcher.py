from flask import Blueprint, current_app, request, jsonify

phone_blueprint = Blueprint("phone", __name__, url_prefix="/api")


@phone_blueprint.route("/phone_tracker", methods=['POST'])
def get_interaction():
   print(request.json)
   return jsonify({ }), 200