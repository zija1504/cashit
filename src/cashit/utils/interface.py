from typing import List, Dict, Union
import inquirer
from marshmallow.exceptions import ValidationError
from .db import get_categories_from_database
from inquirer.themes import GreenPassion
from .fileProcessing import edit_utils
import sys
import os


sys.path.append(os.path.realpath("."))


def interface_add_from_file(temporary_list: List[Dict]) -> List[Dict]:
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
        new_values = interface_edit(items_to_edit, get_categories_from_database())
        edit_utils(temporary_list, items_to_edit, new_values)
        loop_value = inquirer.prompt(
            [inquirer.Confirm("continue", message="Kontynuować edycję?")]
        )
    return temporary_list


def interface_edit(items_to_edit: Dict[str, str], category: List):
    q = [
        inquirer.Text(
            "name", message="Nowa nazwa wydatku", default=items_to_edit["name"][0]
        ),
        inquirer.List("category", message="Wybierz kateogrię", choices=category),
    ]
    new_values = inquirer.prompt(q, theme=GreenPassion())
    return new_values


def interface_new(category: List[Dict]) -> Dict[str, Union[str, float]]:
    q = [
        inquirer.Text("name", message="Nowa nazwa wydatku"),
        inquirer.Text("price", message="Cena wydatku"),
        inquirer.Text("date", message="zakup dokonany, Rok-Mie-Dzi?"),
        inquirer.List("category", message="Wybierz kateogrię", choices=category),
    ]
    new_values = inquirer.prompt(q, theme=GreenPassion())
    return new_values
