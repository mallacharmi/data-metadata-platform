from db import db

class Lineage(db.Model):
    __tablename__ = "lineage"

    id = db.Column(db.Integer, primary_key=True)
    source_dataset_id = db.Column(db.Integer, nullable=False)
    target_dataset_id = db.Column(db.Integer, nullable=False)
    job_name = db.Column(db.String(255), nullable=False)
