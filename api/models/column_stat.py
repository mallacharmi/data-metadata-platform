from db import db

class ColumnStat(db.Model):
    __tablename__ = "column_stats"

    id = db.Column(db.Integer, primary_key=True)

    dataset_id = db.Column(
        db.Integer,
        db.ForeignKey("datasets.id"),
        nullable=False
    )

    column_name = db.Column(db.String, nullable=False)
    null_fraction = db.Column(db.Float)
    distinct_count = db.Column(db.Integer)
