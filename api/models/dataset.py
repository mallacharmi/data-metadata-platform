from datetime import datetime
from db import db

class Dataset(db.Model):
    __tablename__ = "datasets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    tags = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
