"""Commands for click, decorator allow run program from terminal."""

import click

from cashit.settings import dev_db
from cashit.utils.db import create_database, create_new_category
from cashit.utils.general import add_expenses_from_file, add_single_expense


@click.command()
def create_database_cli():
    """Cli version."""
    create_database(dev_db)


@click.command()
def create_new_category_cli():
    """Cli version."""
    create_new_category()


@click.command()
def add_single_expense_cli():
    """Cli version add single expenses."""
    add_single_expense(dev_db)


@click.command()
@click.argument('file', type=click.File())
def add_expenses_from_file_cli(file):
    """Cli version of add expenses."""
    add_expenses_from_file(file)
