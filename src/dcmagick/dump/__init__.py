from enum import Enum
from pathlib import Path

import click

from .json import dump_json
from .pretty import dump_pretty

class Format(Enum):
    PRETTY = 'pretty'
    JSON = 'json'

    def __str__(self):
        return self.value


@click.command()
@click.option("--format", type=str, default=Format.PRETTY)
@click.argument("src", nargs=1)
def dump(format, src: str):
    if not Path(src).exists():
        msg = "{} doesn't exit".format(src)
        click.echo(msg, err=True)

    if format == 'pretty':
        result = dump_pretty(src)
    else:
        result = dump_json(src)
    click.echo(result)