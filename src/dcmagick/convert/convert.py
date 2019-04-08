import click
import numpy as np

from ..common.context import slice_context


@click.command()
@click.option("--wc", type=int, help="Window center")
@click.option("--ww", type=int, help="Window width")
@click.argument("src", type=click.Path(exists=True), nargs=1)
@click.argument("dst", nargs=1)
def convert(wc, ww, src, dst):
    with slice_context(str(src), dst) as slice_proxy:
        pass
