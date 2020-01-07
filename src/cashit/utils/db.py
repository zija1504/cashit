import click
from cashit.model import Category, Item, database
from colorama import init, Fore, Style
from typing import List
from .schema import CategorySchema
from marshmallow import ValidationError


def create_database():
    with database:
        database.create_tables([Category, Item])


def create_new_category():
    init()
    new_category = {}
    print(Fore.GREEN + "Nastepujące kategorie są utworzone:")
    for category in Category.select():
        print(Fore.GREEN + category.name)
    new_category["name"] = input(Fore.CYAN + "Dodaj kateogrię:\n")
    try:
        new_category = CategorySchema().load(new_category)
        Category.create(**new_category)
    except ValidationError as err:
        print(err.messages["name"][0])


def add_item_to_database(**data_dict):
    with database.atomic():
        item = Item.create(
            name=data_dict["name"],
            price=data_dict["price"],
            date=data_dict["date"],
            category=data_dict["category"],
        )
        print(
            f"Dodano do bazy produkt: {item.name}, cena: {item.price}, kategoria: {item.category}"
        )


def get_categories_from_database() -> List:
    category_list = [category.name for category in Category.select()]
    return category_list


def get_items_from_database() -> List:
    items_list = Item.select()
    return [item for item in items_list]
