from marshmallow import Schema, fields

class DatasetSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    tags = fields.Str()
    created_at = fields.DateTime()
