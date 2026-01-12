from db import db

class Column(db.Model):
    __tablename__ = "columns"

    id = db.Column(db.Integer, primary_key=True)

    dataset_id = db.Column(
        db.Integer,
        db.ForeignKey("datasets.id"),
        nullable=False
    )

    name = db.Column(db.String, nullable=False)
    data_type = db.Column(db.String, nullable=False)
