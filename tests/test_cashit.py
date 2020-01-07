from io import StringIO
import os

from click.testing import CliRunner
from peewee import SqliteDatabase
import pytest

from cashit.cli import cli
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


@pytest.fixture
def category(testdb, monkeypatch):
    category_name = StringIO("ogólne\n")
    monkeypatch.setattr("sys.stdin", category_name)
    create_new_category()
    category_name = StringIO("spożywcze\n")
    monkeypatch.setattr("sys.stdin", category_name)
    create_new_category()


items_list = [
    dict(name="woda", price=0.99, date="2020-02-01", category="ogólne"),
    dict(name="woda1", price=1.99, date="2020-02-02", category="spożywcze"),
]


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_add_category(testdb, monkeypatch, capsys):
    category_name = StringIO("chemia\n")
    monkeypatch.setattr("sys.stdin", category_name)
    create_new_category()
    categories = get_categories_from_database()
    assert categories[0] == "chemia"
    category_name = StringIO("woda\n")
    monkeypatch.setattr("sys.stdin", category_name)
    create_new_category()
    categories = get_categories_from_database()
    assert categories[0] == "chemia"
    assert categories[1] == "woda"
    category_name = StringIO("\n")
    monkeypatch.setattr("sys.stdin", category_name)

    create_new_category()
    captured = capsys.readouterr()
    assert "Kategoria nie może być pusta" in captured.out


def test_creating_tables():
    database = db
    create_database()
    database.close()


def test_add_item_to_database(category):
    add_item_to_database(**items_list[0])
    items_from_db = get_items_from_database()
    assert items_from_db[0].name == items_list[0]["name"]
    add_item_to_database(**items_list[1])
    items_from_db = get_items_from_database()
    assert len(items_from_db) == 2
    assert items_from_db[0].name == items_list[0]["name"]
    assert items_from_db[1].price == items_list[1]["price"]
