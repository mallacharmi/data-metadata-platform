from flask import Blueprint, request, jsonify
from models.dataset import Dataset

search_bp = Blueprint("search", __name__)

@search_bp.route("/search", methods=["GET"])
def search_datasets():
    query = request.args.get("q")

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    results = Dataset.query.filter(
        (Dataset.name.ilike(f"%{query}%")) |
        (Dataset.tags.ilike(f"%{query}%"))
    ).all()

    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "description": d.description,
            "tags": d.tags
        }
        for d in results
    ]), 200
