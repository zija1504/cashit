from cashit.cli import cli
from click.testing import CliRunner


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
