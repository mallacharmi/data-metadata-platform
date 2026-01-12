from flask import Blueprint, request, jsonify
from db import db

from models.dataset import Dataset
from models.column import Column
from models.column_stat import ColumnStat
from models.run import Run
from models.dq_result import DataQualityResult

from schemas.dataset_schema import DatasetSchema

dataset_bp = Blueprint("datasets", __name__)

dataset_schema = DatasetSchema()
datasets_schema = DatasetSchema(many=True)


# -----------------------------
# POST /datasets
# -----------------------------
@dataset_bp.route("/datasets", methods=["POST"])
def create_dataset():
    data = request.get_json()

    existing = Dataset.query.filter_by(name=data["name"]).first()
    if existing:
        return jsonify(dataset_schema.dump(existing)), 200

    dataset = Dataset(
        name=data["name"],
        description=data.get("description"),
        tags=data.get("tags")
    )

    db.session.add(dataset)
    db.session.commit()

    return jsonify(dataset_schema.dump(dataset)), 201


# -----------------------------
# GET /datasets/<id>
# -----------------------------
@dataset_bp.route("/datasets/<int:dataset_id>", methods=["GET"])
def get_dataset(dataset_id):
    dataset = Dataset.query.get(dataset_id)

    if not dataset:
        return jsonify({"error": "Dataset not found"}), 404

    # Fetch schema
    columns = Column.query.filter_by(dataset_id=dataset_id).all()

    # Fetch runs
    runs = Run.query.filter_by(dataset_id=dataset_id).order_by(Run.id.asc()).all()

    # ✅ Fetch ALL DQ results for this dataset
    dq_results = DataQualityResult.query.filter_by(dataset_id=dataset_id).all()

    response = {
        "dataset": dataset_schema.dump(dataset),
        "schema": [
            {"name": c.name, "type": c.data_type}
            for c in columns
        ],
        "runs": [
            {
                "id": r.id,
                "job_name": r.job_name,
                "status": r.status
            }
            for r in runs
        ],
        # ✅ THIS IS THE MISSING PART FOR 100%
        "data_quality_results": [
            {
                "check_name": d.check_name,
                "status": d.status,
                "success_percentage": d.success_percentage
            }
            for d in dq_results
        ]
    }

    return jsonify(response), 200


# -----------------------------
# POST /datasets/<id>/schema
# -----------------------------
@dataset_bp.route("/datasets/<int:dataset_id>/schema", methods=["POST"])
def add_schema_and_stats(dataset_id):
    data = request.get_json()

    dataset = Dataset.query.get(dataset_id)
    if not dataset:
        return jsonify({"error": "Dataset not found"}), 404

    Column.query.filter_by(dataset_id=dataset_id).delete()
    ColumnStat.query.filter_by(dataset_id=dataset_id).delete()

    for col in data.get("schema", []):
        db.session.add(
            Column(
                dataset_id=dataset_id,
                name=col["name"],
                data_type=col["data_type"]   # ✅ FIXED
            )
        )

    for stat in data.get("stats", []):
        db.session.add(
            ColumnStat(
                dataset_id=dataset_id,
                column_name=stat["column"],
                null_fraction=stat["null_fraction"],
                distinct_count=stat["distinct_count"]
            )
        )

    db.session.commit()
    return jsonify({"message": "Schema and stats stored"}), 201
