import click
import numpy as np

from ..common.context import slice_context
from ..common.window import assign as assign_window


@click.command()
@click.option("--window", type=str, help="Window configuration")
@click.argument("src", type=click.Path(exists=True), nargs=1)
@click.argument("dst", nargs=1)
def convert(window, src, dst):
    with slice_context(str(src), dst) as slice_proxy:
        assign_window(slice_proxy, window)
