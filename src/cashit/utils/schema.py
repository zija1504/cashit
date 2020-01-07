from marshmallow import Schema, fields, validate


class ItemSchema(Schema):
    name = fields.Str(
        required=True, validate=validate.Length(min=1, error="Nazwa nie może być pusta")
    )
    price = fields.Float(required=True)
    date = fields.Str(required=True, validate=validate.Regexp(r"\d{4}-\d{2}-\d{2}"))
    category = fields.Str(required=True)


class CategorySchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Kategoria nie może być pusta"),
    )
