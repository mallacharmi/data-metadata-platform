from flask import Blueprint, request, jsonify
from models.run import Run
from db import db
from datetime import datetime

run_bp = Blueprint("runs", __name__)

@run_bp.route("/runs", methods=["POST"])
def create_run():
    data = request.json

    run = Run(
        job_name=data["job_name"],
        status=data["status"],
        dataset_id=data["dataset_id"],
        finished_at=datetime.utcnow() if data["status"] == "COMPLETE" else None
    )

    db.session.add(run)
    db.session.commit()

    return jsonify({"run_id": run.id}), 201
