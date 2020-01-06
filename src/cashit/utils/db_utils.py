import click
from cashit.model import Category, Item, database
from colorama import init, Fore, Style
from typing import List


@click.command()
def create_database():
    with database:
        database.create_tables([Category, Item])


@click.command()
def create_new_category():
    init()
    print(Fore.GREEN + "Nastepujące kategorie są utworzone:")
    for category in Category.select():
        print(Fore.GREEN + category.name)
    name = input(Fore.CYAN + "Add new category:\n")
    Category.create(name=name)


def add_item_to_database(**data_dict):
    with database.atomic():
        item = Item.create(**data_dict)
        print(
            f"Dodano do bazy produkt: {item.name}, cena: {item.price}, kategoria: {item.category}"
        )


def get_categories_from_database() -> List:
    category_list = [category.name for category in Category.select()]
    return category_list
