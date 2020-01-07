import click
from cashit.utils.general import add_expenses_from_file, add_single_expense
from cashit.utils.db import create_database, create_new_category


@click.command()
def create_database_cli():
    create_database()


@click.command()
def create_new_category_cli():
    create_new_category()


@click.command()
def add_single_expense_cli():
    add_single_expense()


@click.command()
@click.argument("file", type=click.File())
def add_expenses_from_file_cli(file):
    add_expenses_from_file(file)
