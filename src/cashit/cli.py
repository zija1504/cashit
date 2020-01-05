import click
from .addExpanse.expanse import add_expanse


@click.group()
def cli():
    """Command line interface for the cashit package"""


cli.add_command(add_expanse)

if __name__ == "__main__":
    cli()
