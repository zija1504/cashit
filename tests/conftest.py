import pytest

from peewee import SqliteDatabase
from cashit.model import Category, Item
from cashit.utils.db import (
    get_categories_from_database,
    create_new_category,
    create_database,
    add_item_to_database,
    get_items_from_database,
)


MODELS = [Category, Item]
# use an in-memory SQLite for tests.
db = SqliteDatabase(":memory:")


@pytest.fixture
def testdb():
    db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    db.connect()
    db.create_tables(MODELS)
    yield db
    # Not strictly necessary since SQLite in-memory databases only live
    # for the duration of the connection, and in the next step we close
    # the connection...but a good practice all the same.
    db.drop_tables(MODELS)
    # Close connection to db.
    db.close()


@pytest.fixture()
def createdb():
    db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    yield db
    db.close()


@pytest.fixture
def preprocess():
    listSuccess = ["2020-01-02", "mleko: 2,34", "woda: 2.01", "woda: 2,01"]
    yield listSuccess
