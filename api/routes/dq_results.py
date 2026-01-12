from flask import Blueprint, request, jsonify
from db import db
from models.dq_result import DataQualityResult

dq_bp = Blueprint("dq", __name__)


@dq_bp.route("/dq-results", methods=["POST"])
def add_dq_result():
    data = request.get_json()

    dq = DataQualityResult(
        dataset_id=data["dataset_id"],
        check_name=data["check_name"],
        status=data["status"],
        success_percentage=data["success_percentage"]
    )

    db.session.add(dq)
    db.session.commit()

    return jsonify({"message": "DQ result stored"}), 201
