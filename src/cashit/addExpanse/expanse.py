from datetime import date
import os
import re
import sys
from collections import defaultdict
from pprint import pprint
from typing import DefaultDict, Dict, List, TextIO, Tuple

import click
from inquirer.themes import GreenPassion
import inquirer
import readchar

from cashit.utils import add_item_to_database, get_categories_from_database

sys.path.append(os.path.realpath("."))


@click.command()
@click.argument("file", type=click.File())
def add_expenses(file: TextIO):
    temporary_list = file.read().strip().split("\n")
    temporary_list = pre_processing(temporary_list)
    temporary_list = interactive_add(temporary_list)
    postprocessing(temporary_list)


def pre_processing(temporary_list: List[str]) -> List[Dict]:
    _date = temporary_list.pop(0)
    temporary_list = [item.strip().replace(",", ".") for item in temporary_list]
    item_name_re = re.compile(r"(^[a-żA-Ż\s]*)(?:)")  # like ser żółty
    item_price_re = re.compile(r"(\d*\.\d*)")  # cena
    items: DefaultDict[str, float] = DefaultDict(float)
    for item in temporary_list:
        try:
            item_name = item_name_re.search(item).group(0)
            item_price = float(item_price_re.search(item).group(0))
            items[item_name] += item_price
        except Exception as e:
            print(e)
    items_list = [
        dict(name=k, price=v, date=_date, category="ogólne") for k, v in items.items()
    ]
    return items_list


def interactive_add(temporary_list: List[Dict]) -> List[Dict]:
    message = "Po wstępnej obróbce nazwy wydatków zaznacz by edytować, scalić, dodać kategorię"
    loop_value = {}
    loop_value["continue"] = True
    while loop_value["continue"]:
        questions = [
            inquirer.Checkbox(
                "name",
                message=message,
                choices=list(map(lambda y: y["name"], temporary_list)),
                default=[],
            )
        ]

        items_to_edit = inquirer.prompt(questions)
        new_values = interactive_edit(get_categories_from_database())
        edit_utils(temporary_list, items_to_edit, new_values)
        loop_value = inquirer.prompt(
            [inquirer.Confirm("continue", message="Kontynuować edycję")]
        )
    return temporary_list


def postprocessing(temporary_list: List[Dict]):
    for data_dict in temporary_list:
        add_item_to_database(**data_dict)


def interactive_edit(category: List):
    q = [
        inquirer.Text("name", message="Nowa nazwa wydatku"),
        inquirer.List("category", message="Wybierz kateogrię", choices=category),
    ]
    new_values = inquirer.prompt(q, theme=GreenPassion())
    return new_values


def edit_utils(temporaryList: List[Dict], items_to_edit: Dict, new_values: Dict):
    price = 0
    _date = temporaryList[0]["date"]
    for name in items_to_edit["name"]:
        for index, x in enumerate(temporaryList):
            if name == x["name"]:
                price += x["price"]
                temporaryList.pop(index)

    temporaryList.append(
        dict(
            name=new_values["name"],
            price=price,
            date=_date,
            category=new_values["category"],
        )
    )
