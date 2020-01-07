from cashit.settings import SQL_PATH
from peewee import (
    ForeignKeyField,
    SqliteDatabase,
    Model,
    CharField,
    FloatField,
    DateField,
)
import json

database: database = SqliteDatabase(SQL_PATH)


# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = database


class Category(BaseModel):
    name = CharField(unique=True, null=False)

    def __str__(self):
        return self.name


class Item(BaseModel):
    name = CharField(null=False)
    price = FloatField(null=False)
    date = DateField(null=False)
    category = ForeignKeyField(Category, field=Category.name, backref="items")
