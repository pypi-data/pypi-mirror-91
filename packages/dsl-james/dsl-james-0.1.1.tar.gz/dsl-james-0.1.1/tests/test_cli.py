import pytest
from click.testing import CliRunner

from james.cli import main


@pytest.fixture(scope='session')
def cli_runner():
    """Fixture that returns a helper function to run the cookiecutter cli."""
    runner = CliRunner()

    def cli_main(*cli_args, **cli_kwargs):
        """Run cookiecutter cli main with the given args."""
        return runner.invoke(main, *cli_args, **cli_kwargs)

    return cli_main


def test_cli_version(cli_runner):
    """Verify correct version output by `james --version` on cli invocation."""
    result = cli_runner('--version')
    assert result.exit_code == 0
    assert 'version' in result.output


def test_cli_help(cli_runner):
    result = cli_runner('--help')
    assert result.exit_code == 0
    assert result.output.startswith('Usage:')



