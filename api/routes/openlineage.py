from flask import Blueprint, request, jsonify
from models.lineage import Lineage
from db import db

openlineage_bp = Blueprint("openlineage", __name__)

@openlineage_bp.route("/openlineage/events", methods=["POST"])
def receive_openlineage_event():
    event = request.get_json()

    # SAFETY: ignore events without datasets
    inputs = event.get("inputs", [])
    outputs = event.get("outputs", [])

    if not inputs or not outputs:
        return jsonify({"status": "ignored"}), 200

    return jsonify({"status": "processed"}), 200

