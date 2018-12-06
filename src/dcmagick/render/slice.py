from pathlib import Path

import click

from ..util import read_dcms


@click.command()
@click.option('--wc', type=int, help='Window center')
@click.option('--ww', type=int, help='Window width')
@click.option('--cmap', type=int, help='Window width')
@click.option('--gsps', type=str, multiple=True, help='Grayscale SoftCopy Presentation State Storage files')
@click.option('--kos', type=str, multiple=True, help='Grayscale SoftCopy Presentation State Storage files')
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
def render(wc, ww, pr, src, dst):
    dcms = read_dcms(src)
    # dcms.sort(key=slice_location_order)

    prs = pr and read_dcms(pr)
    if prs is not None:
        pass

    for i, (path, dcm) in enumerate(dcms):
        p = Path(dst)
        dst_path = p.parent / '{}_{}{}'.format(p.stem, i, p.suffix)
        print(str(dst_path))
    click.echo('render')
    click.echo(wc is None)
    click.echo(pr)
    click.echo(src)
    click.echo(dst)