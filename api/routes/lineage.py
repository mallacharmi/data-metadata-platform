from flask import Blueprint, jsonify, request
from db import db
from models.lineage import Lineage

lineage_bp = Blueprint("lineage", __name__)

# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------
@lineage_bp.route("/health/lineage", methods=["GET"])
def lineage_health():
    return jsonify({"status": "lineage service ready"}), 200


# --------------------------------------------------
# CREATE LINEAGE (CALLED BY PIPELINE)
# --------------------------------------------------
@lineage_bp.route("/lineage", methods=["POST"])
def create_lineage():
    data = request.json

    existing = Lineage.query.filter_by(
        source_dataset_id=data["source_dataset_id"],
        target_dataset_id=data["target_dataset_id"],
        job_name=data["job_name"]
    ).first()

    if existing:
        return jsonify({"message": "Lineage already exists"}), 200

    lineage = Lineage(
        source_dataset_id=data["source_dataset_id"],
        target_dataset_id=data["target_dataset_id"],
        job_name=data["job_name"]
    )

    db.session.add(lineage)
    db.session.commit()

    return jsonify({"message": "Lineage created"}), 201

# --------------------------------------------------
# GET LINEAGE FOR A DATASET
# --------------------------------------------------
@lineage_bp.route("/datasets/<int:dataset_id>/lineage", methods=["GET"])
def get_lineage(dataset_id):
    upstream = Lineage.query.filter_by(
        target_dataset_id=dataset_id
    ).all()

    downstream = Lineage.query.filter_by(
        source_dataset_id=dataset_id
    ).all()

    return jsonify({
        "dataset_id": dataset_id,
        "upstream": [
            {
                "dataset_id": l.source_dataset_id,
                "job": l.job_name
            }
            for l in upstream
        ],
        "downstream": [
            {
                "dataset_id": l.target_dataset_id,
                "job": l.job_name
            }
            for l in downstream
        ]
    }), 200
