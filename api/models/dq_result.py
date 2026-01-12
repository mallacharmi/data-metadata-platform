from db import db

class DataQualityResult(db.Model):
    __tablename__ = "data_quality_results"

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, nullable=False)
    check_name = db.Column(db.String(255))
    status = db.Column(db.String(50))
    success_percentage = db.Column(db.Integer)
