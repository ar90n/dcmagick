from enum import Enum
from pathlib import Path

import click

from .json import dump_json
from .pretty import dump_pretty
from .braille import dump_braille


from ..common.context import slice_context


class Format(Enum):
    PRETTY = "pretty"
    JSON = "json"
    BRAILLE = "braille"

    def __str__(self):
        return self.value


@click.command()
@click.option("--format", type=str, default=Format.PRETTY)
@click.argument("src", nargs=1)
def dump(format, src: str):
    with slice_context(src, None) as proxy_and_param:
        slice_proxy, _ = proxy_and_param
        if format == "pretty":
            result = dump_pretty(slice_proxy)
        elif format == "json":
            result = dump_json(slice_proxy)
        else:
            result = dump_braille(slice_proxy)
        click.echo(result)
