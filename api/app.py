from flask import Flask, jsonify
from db import db

# Import models so SQLAlchemy creates tables
from models.dataset import Dataset
from models.column import Column
from models.column_stat import ColumnStat
from models.lineage import Lineage
from models.run import Run
from models.dq_result import DataQualityResult

# Import blueprints
from routes.datasets import dataset_bp
from routes.search import search_bp
from routes.lineage import lineage_bp
from routes.openlineage import openlineage_bp
from routes.runs import run_bp
from routes.dq_results import dq_bp

# ------------------------
# Flask App Initialization
# ------------------------
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:postgres@metadata-postgres:5432/metadata"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ------------------------
# Create Tables
# ------------------------
with app.app_context():
    db.create_all()

# ------------------------
# Health Check (CRITICAL)
# ------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# ------------------------
# Register Blueprints
# ------------------------
app.register_blueprint(dataset_bp)
app.register_blueprint(search_bp)
app.register_blueprint(lineage_bp)
app.register_blueprint(openlineage_bp)
app.register_blueprint(run_bp)
app.register_blueprint(dq_bp)

# ------------------------
# App Runner
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
