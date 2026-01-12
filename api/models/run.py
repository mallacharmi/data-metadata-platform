from db import db
from datetime import datetime

class Run(db.Model):
    __tablename__ = "runs"

    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(100))
    status = db.Column(db.String(20))
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime)

    dataset_id = db.Column(db.Integer, db.ForeignKey("datasets.id"))
