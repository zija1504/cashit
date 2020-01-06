import click
from .addExpanse.expanse import add_expenses
from .utils import create_database, create_new_category


@click.group()
def cli():
    """Command line interface for the cashit package"""


cli.add_command(add_expenses)
cli.add_command(create_database)
cli.add_command(create_new_category)
if __name__ == "__main__":
    cli()
