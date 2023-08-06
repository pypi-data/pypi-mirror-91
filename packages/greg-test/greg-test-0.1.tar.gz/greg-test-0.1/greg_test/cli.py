"""
greg-test
"""

from typing import Any

import click
from pudb import set_trace as bp  # pylint: disable=unused-import

from greg_test import NAME, __version__, core

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def print_version(ctx: Any, param: Any, value: Any) -> None:
    """Show version."""

    # pylint: disable=unused-argument

    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option(
    "-v",
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show version",
)
def cli() -> None:
    """
    greg-test description.
    """


@cli.command()
@click.argument("name", required=True)
@click.option(
    "-d",
    "--demo",
    default="default",
    help="Print argument.",
)
def demo(name: str, demo: str) -> None:
    """Command description"""
    core.demo(name, demo)


@cli.command()
@click.argument("value", required=True, type=float)
def power(value: float) -> None:
    """Compute power"""
    core.power(value)


def main() -> None:
    cli(prog_name=NAME)  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg


if __name__ == "__main__":
    main()
