"""Model schema for database."""

from peewee import CharField, DateField, FloatField, ForeignKeyField, Model

from cashit.settings import dev_db

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatic
# use the correct storage.


class BaseModel(Model):
    """Base model.

    Args:
        Model ([type]): [description]
    """

    class Meta(object):
        """Meta.

        Args:
            object ([type]): [description]
        """
        database = dev_db


class Category(BaseModel):
    """Category model.

    Args:
        BaseModel ([type]): [description]

    Returns:
        [type]: [description]
    """

    name = CharField(unique=True, null=False)


class Item(BaseModel):
    """Item model.

    Args:
        BaseModel ([type]): [description]
    """

    name = CharField(null=False)
    price = FloatField(null=False)
    date = DateField(null=False)
    category = ForeignKeyField(Category, field=Category.name, backref='items')
