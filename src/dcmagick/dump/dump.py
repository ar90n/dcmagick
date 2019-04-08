from enum import Enum

import click

from ..common.context import slice_context
from .json import dump as dump_json
from .pretty import dump as dump_pretty
from .terminal import dump_braille, dump_halfblock, dump_iterm2


class Format(Enum):
    PRETTY = "pretty"
    JSON = "json"
    BRAILLE = "braille"
    HALFBLOCK = "halfblock"
    ITERM2 = "iterm2"


def _get_dump_func(format: Format):
    return {
        Format.PRETTY: dump_pretty,
        Format.JSON: dump_json,
        Format.BRAILLE: dump_braille,
        Format.HALFBLOCK: dump_halfblock,
        Format.ITERM2: dump_iterm2,
    }[format]


@click.command()
@click.option(
    "--format",
    type=click.Choice(Format.__members__),
    callback=lambda c, p, v: getattr(Format, v) if v else None,
    default=Format.PRETTY,
)
@click.argument("src", type=click.Path(exists=True), nargs=1)
def dump(format, src: str):
    with slice_context(src, None) as slice_proxy:
        dump_func = _get_dump_func(format)
        click.echo(dump_func(slice_proxy))
