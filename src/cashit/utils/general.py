from typing import TextIO
from marshmallow.exceptions import ValidationError
from .fileProcessing import pre_processing, postprocessing
from .interface import interface_add_from_file, interface_new
from .db import get_categories_from_database, add_item_to_database, database
from .schema import ItemSchema


def add_expenses_from_file(database, file: TextIO):
    temporary_list = file.read().strip().split("\n")
    temporary_list = pre_processing(temporary_list)
    list_from_interface = interface_add_from_file(temporary_list)
    try:
        temporary_list = ItemSchema(many=True).load(list_from_interface)
        postprocessing(database, temporary_list)
    except ValidationError as err:
        print(err)


def add_single_expense():
    new_values = interface_new(get_categories_from_database())
    try:
        new_values = ItemSchema().load(new_values)
        add_item_to_database(database, **new_values)
    except ValidationError as err:
        for val in err.messages.values():
            print(val[0])
