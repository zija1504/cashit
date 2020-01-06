from cashit.cli import cli
from click.testing import CliRunner
from cashit.addExpense import add_expenses
import pytest


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
