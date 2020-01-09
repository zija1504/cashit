import os
from contextlib import contextmanager
from io import StringIO

import pytest
from click.testing import CliRunner
from tests.conftest import mocking_interface_failure, mocking_interface_success

from cashit.cli import cli
from cashit.utils import general
from cashit.utils.db import (
    add_item_to_database,
    create_database,
    create_new_category,
    get_categories_from_database,
    get_items_from_database,
)
from cashit.utils.fileProcessing import (
    edit_utils,
    get_date,
    match_item_name_and_price,
    postprocessing,
    pre_processing,
)
from cashit.utils.general import add_expenses_from_file


@contextmanager
def does_not_raise():
    yield


items_list = [
    dict(name='woda', price=0.98, date='2020-02-01', category='ogólne'),
    dict(name='woda1', price=1.98, date='2020-02-02', category='spożywcze'),
]


def test_cli():  # noqa
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_add_category(testdb, monkeypatch, capsys):
    category_name = StringIO('chemia\n')
    monkeypatch.setattr('sys.stdin', category_name)
    create_new_category()  # noqa
    categories = get_categories_from_database()
    assert categories[0] == 'chemia'
    category_name = StringIO('woda\n')
    monkeypatch.setattr('sys.stdin', category_name)
    create_new_category()
    categories = get_categories_from_database()
    assert categories[0] == 'chemia'
    assert categories[1] == 'woda'
    category_name = StringIO('\n')
    monkeypatch.setattr('sys.stdin', category_name)

    create_new_category()
    captured = capsys.readouterr()
    assert 'Wrong data' in captured.out


def test_creating_tables(createdb):
    create_database(createdb)


def test_add_item_to_database(testdb, monkeypatch):
    category_name = StringIO('ogólne\n')
    monkeypatch.setattr('sys.stdin', category_name)
    create_new_category()
    category_name = StringIO('spożywcze\n')
    monkeypatch.setattr('sys.stdin', category_name)
    create_new_category()
    add_item_to_database(testdb, **items_list[0])
    items_from_db = get_items_from_database()
    assert items_from_db[0].name == items_list[0]['name']
    add_item_to_database(testdb, **items_list[1])
    items_from_db = get_items_from_database()
    assert len(items_from_db) == 2
    assert items_from_db[0].name == items_list[0]['name']
    assert items_from_db[1].price == items_list[1]['price']


@pytest.mark.parametrize(
    'inputs, expected', [(['2020-01-02'], '2020-01-02'),
                         (['2020-10-20'], '2020-10-20'),
                         ])
def test_get_date_success(inputs, expected):
    assert get_date(inputs) == expected


@pytest.mark.parametrize('inputs', [['2020-1-1'], ['10-10-10'], ['Mąka: 4,3']])
def test_get_date_exception(inputs):
    with pytest.raises(Exception, match='No date format in first line of file'):
        get_date(inputs)


@pytest.mark.parametrize(
    'inputs, expect',
    [
        (['mąka: 4.34', 'cukier: 2.33'], does_not_raise()),
        (['chleb pszenny: 4.3', 'cukier brązowy: 2.99'], does_not_raise()),
        ([' 4.34', 'cukier: 2,33'], pytest.raises(AttributeError)),
        (['mąka: 4.34', 'cukier:'], pytest.raises(AttributeError)),
    ],
)
def test_match_item_name_and_price_exception(inputs, expect):
    with expect:
        match_item_name_and_price(inputs)


@pytest.mark.parametrize(
    'inputs, expect',
    [
        (['2020-01-03', 'mąka: 4.34', 'cukier: 2,33'], does_not_raise()),
        (
            ['2021-03-05', 'chleb pszenny: 4.3', 'cukier brązowy: 2.99'],
            does_not_raise(),
        ),
        (['2020-02-02', ' 4.34', 'cukier: 2,33'], pytest.raises(AttributeError)),
        (['20-20-20', 'mąka: 4.34', 'cukier:2,33'], pytest.raises(Exception)),
    ],
)
def test_preprocessing_exception(inputs, expect):
    with expect:
        pre_processing(inputs)


def test_preprocessing_output():
    output = pre_processing(['2020-02-03', 'mąka: 4,34', 'mąka: 2.00'])
    assert len(output) == 1
    assert output[0]['price'] == 6.34


def test_edit_utils():
    inputsList = [
        dict(name='sól jodowana', price=2, date='2021-01-03', category='ogólne'),
        dict(name='sól', price=1, date='2020-01-03', category='ogólne'),
    ]
    new_values = dict(name='sól morska', category='spożywcze')
    edit_utils(inputsList, {'name': ['sól']}, new_values)
    print(inputsList)
    assert inputsList[1]['name'] == 'sól morska'
    new_values = dict(name='sól nowa', category='spożywcze')
    edit_utils(
        inputsList, {'name': ['sól morska', 'sól jodowana']}, new_values)
    assert len(inputsList) == 1


def test_postprocessing_(testdb, monkeypatch, createdb):
    category_name = StringIO('ogólne\n')
    monkeypatch.setattr('sys.stdin', category_name)
    create_new_category()
    category_name = StringIO('spożywcze\n')
    monkeypatch.setattr('sys.stdin', category_name)
    create_new_category()
    postprocessing(createdb, items_list)
    items = get_items_from_database()
    assert len(items) == 2


def test_successfully_add_expenses_from_file(testdb, createdb, tmpdir, monkeypatch):
    category_name = StringIO('chemiczne\n')
    monkeypatch.setattr('sys.stdin', category_name)
    create_new_category()
    category_name = StringIO('spożywcze\n')
    monkeypatch.setattr('sys.stdin', category_name)
    create_new_category()
    d = tmpdir.mkdir('subdir')
    test = d.join('test.txt')
    test.write(
        """
2020-01-02
Mleko UHT: 6,27
KoncSilant: 8,99
Mąka: 2,95
    """
    )
    monkeypatch.setattr(general, 'interface_add_from_file',
                        mocking_interface_success)
    add_expenses_from_file(createdb, test)
    items = get_items_from_database()
    assert len(items) == 3
    monkeypatch.setattr(general, 'interface_add_from_file',
                        mocking_interface_failure)
    add_expenses_from_file(createdb, test)
    items = get_items_from_database()
    assert len(items) == 3
