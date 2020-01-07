import click
from .command import (
    add_expenses_from_file_cli,
    create_database_cli,
    create_new_category_cli,
    add_single_expense_cli,
)


@click.group()
def cli():
    """Command line interface for the cashit package"""


cli.add_command(add_expenses_from_file_cli)
cli.add_command(create_database_cli)
cli.add_command(create_new_category_cli)
cli.add_command(add_single_expense_cli)
if __name__ == "__main__":
    cli()
