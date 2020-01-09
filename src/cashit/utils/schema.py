"""Module for perform validation."""
from marshmallow import Schema, ValidationError, fields, validate


class ItemSchema(Schema):
    """Schema to validate item json.

    Parameters
    ----------
    Schema : [type]
        [description]
    """

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, error='Nazwa nie może być pusta')
    )
    price = fields.Float(required=True)
    date = fields.Str(
        required=True, validate=validate.Regexp(r'\d{4}-\d{2}-\d{2}'))
    category = fields.Str(required=True)


class CategorySchema(Schema):
    """Schema to validate category json.

    Parameters
    ----------
    Schema : [type]
        [description]
    """

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, error='Kategoria nie może być pusta'),
    )


def validate_input(validator, input_data):
    """Serilazer based on marshmallow schema.

    Args:
        validator ([type]): [description]
        input_data ([type]): [description]

    Returns:
        [type]: [description]
    """
    try:
        return validator.load(input_data)
    except ValidationError as err:
        print('Wrong data: {0}'.format(err.messages))
        return None
