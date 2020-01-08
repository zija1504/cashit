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


def mocking_interface_success(tmpList):
    return [
        dict(name="Mleko UHT", price=6.27, date="2020-01-02", category="spożywcze"),
        dict(name="KoncSilant", price=8.99, date="2020-01-02", category="chemiczne"),
        dict(name="Mąka", price=2.95, date="2020-01-02", category="spożywcze"),
    ]


def mocking_interface_failure(tmpList):
    return [
        dict(name="Mleko UHT", price=6.27, date="2020-01-02", category="spożywcze"),
        dict(name="KoncSilant", price=8.99, date="error", category="chemiczne"),
        dict(name="Mąka", price="error", date="2020-01-02", category="spożywcze"),
    ]
