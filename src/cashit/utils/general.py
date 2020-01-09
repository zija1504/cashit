"""General function for retrieval data."""

from typing import TextIO

from cashit.utils.db import add_item_to_database, get_categories_from_database
from cashit.utils.fileProcessing import postprocessing, pre_processing
from cashit.utils.interface import interface_add_from_file, interface_new
from cashit.utils.schema import ItemSchema, validate_input


def add_expenses_from_file(database, file: TextIO):
    """Multiple expenses.

    Args:
        database ([type]): [description]
        file (TextIO): [description]
    """
    temporary_list = file.read().strip().split('\n')
    temporary_list = pre_processing(temporary_list)
    list_from_interface = interface_add_from_file(temporary_list)
    temporary_list = validate_input(ItemSchema(many=True), list_from_interface)
    if temporary_list:
        postprocessing(database, temporary_list)


def add_single_expense(database):
    """One item per call.

    Args:
        database ([type]): [description]
    """
    new_values = interface_new(get_categories_from_database())
    new_values = validate_input(ItemSchema(), new_values)
    if new_values:
        add_item_to_database(database, **new_values)
