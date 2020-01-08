from contextlib import contextmanager
from io import StringIO
import os

from click.testing import CliRunner
import pytest

from cashit.cli import cli
from cashit.model import Category, Item
from cashit.utils.db import (
    add_item_to_database,
    create_database,
    create_new_category,
    get_categories_from_database,
    get_items_from_database,
)
from cashit.utils.fileProcessing import get_date, match_item_name_and_price


@contextmanager
def does_not_raise():
    yield


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


def test_creating_tables(createdb):
    create_database(createdb)


def test_add_item_to_database(testdb, monkeypatch):
    category_name = StringIO("ogólne\n")
    monkeypatch.setattr("sys.stdin", category_name)
    create_new_category()
    category_name = StringIO("spożywcze\n")
    monkeypatch.setattr("sys.stdin", category_name)
    create_new_category()
    add_item_to_database(testdb, **items_list[0])
    items_from_db = get_items_from_database()
    assert items_from_db[0].name == items_list[0]["name"]
    add_item_to_database(testdb, **items_list[1])
    items_from_db = get_items_from_database()
    assert len(items_from_db) == 2
    assert items_from_db[0].name == items_list[0]["name"]
    assert items_from_db[1].price == items_list[1]["price"]


@pytest.mark.parametrize(
    "input, expected", [(["2020-01-02"], "2020-01-02"), (["2020-10-20"], "2020-10-20")]
)
def test_get_date_success(input, expected):
    assert get_date(input) == expected


@pytest.mark.parametrize("input", [["2020-1-1"], ["10-10-10"], ["Mąka: 4,3"]])
def test_get_date_exception(input):
    with pytest.raises(Exception, match="No date format in first line of file"):
        get_date(input)


@pytest.mark.parametrize(
    "input, expect",
    [
        (["mąka: 4.34", "cukier: 2.33"], does_not_raise()),
        (["chleb pszenny: 4.3", "cukier brązowy: 2.99"], does_not_raise()),
        ([" 4.34", "cukier: 2,33"], pytest.raises(AttributeError)),
        (["mąka: 4.34", "cukier:"], pytest.raises(AttributeError)),
    ],
)
def test_match_item_name_and_price_exception(input, expect):
    with expect:
        match_item_name_and_price(input)
