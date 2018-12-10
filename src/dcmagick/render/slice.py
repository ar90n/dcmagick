from enum import Enum
from pathlib import Path
from itertools import count

import click
import numpy as np
import skimage
from pydicom import dcmread

from ..util import read_dcms

class OutputFormat(Enum):
    JPEG = '.jpg'


def _get_format(path):
    path = Path(path)
    if path.suffix == OutputFormat.JPEG.value:
        return OutputFormat.JPEG
    raise ValueError('Not supported format: {}'.format(path.suffix))


def slice_loader(src, dst):
    if len(src) == 1:
        dcm = dcmread(src[0])
        yield Path(dst), dcm
        return

    dst_path = Path(dst)
    for i, src_loc in enumerate(src):
        dcm = dcmread(src_loc)
        output_path = dst_path.parent / '{}_{}{}'.format(dst_path.stem, i, dst_path.suffix)
        yield output_path, dcm


@click.command()
@click.option('--wc', type=int, help='Window center')
@click.option('--ww', type=int, help='Window width')
@click.option('--cmap', type=int, help='Window width')
@click.option('--gsps', type=str, multiple=True, help='Grayscale SoftCopy Presentation State Storage files')
@click.option('--kos', type=str, multiple=True, help='Grayscale SoftCopy Presentation State Storage files')
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
def render(wc, ww, cmap, gsps, kos, src, dst):
    format = _get_format(dst)

    for path, dcm in slice_loader(src, dst):
        tmp = 255.0 * (dcm.pixel_array - np.min(dcm.pixel_array)) / (np.max(dcm.pixel_array) - np.min(dcm.pixel_array))
        tmp = tmp.astype(np.uint8)
        skimage.io.imsave(path, tmp)