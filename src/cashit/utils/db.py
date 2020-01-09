"""module for processing database."""

from typing import List

from cashit.model import Category, Item
from cashit.utils.schema import CategorySchema, validate_input


def create_database(database):
    """Creating default database."""
    with database:
        database.create_tables([Category, Item])


def _cli_category_from_db():
    """Printing categories from db."""
    print('Nastepujące kategorie są utworzone:')
    print('{0}'.format(get_categories_from_database()))
    return input('Dodaj kateogrię:\n')


def create_new_category():
    """Create new category of items in cli."""
    new_category = _cli_category_from_db()
    validated = validate_input(CategorySchema(), {'name': new_category})
    if validated:
        Category.create(**validated)


def add_item_to_database(database, **data_dict):
    """Add item to db with fast atomic way."""
    with database.atomic():
        item = Item.create(
            name=data_dict['name'],
            price=data_dict['price'],
            date=data_dict['date'],
            category=data_dict['category'],
        )
        print('Dodano do bazy produkt: {0}, cena: {1},kategoria: {2} '.format(
            item.name, item.price, item.category,
        ))


def get_categories_from_database() -> List:
    """return list of categories created.

    Returns
    -------
    List
        [categories of item]
    """
    return [category.name for category in Category.select()]


def get_items_from_database() -> List:
    """Returs all items from db.

    Returns
    -------
    List
        [description]
    """
    items_list = Item.select()
    return list(items_list)
