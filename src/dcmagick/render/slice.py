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


def calc_window(pixel_array, *, wc=None, ww=None):
    minv = np.min(pixel_array)
    maxv = np.max(pixel_array)

    wc = (maxv + minv) // 2 if wc is None else wc
    ww = 2 * min(abs(minv - wc), abs(maxv - wc)) if ww is None else ww
    return wc, ww


def apply_window(pixel_array, wc, ww):
    half_width = ww // 2
    minv = wc - half_width
    maxv = wc + half_width

    window_applied = pixel_array.copy()
    window_applied[pixel_array < minv] = minv
    window_applied[maxv < pixel_array] = maxv
    window_applied = 255.0 * (window_applied - minv) / (maxv - minv)
    window_applied = window_applied.astype(np.uint8)
    return window_applied


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
        wc, ww = calc_window(dcm.pixel_array, wc=wc, ww=ww)
        buffer = apply_window(dcm.pixel_array, wc, ww)
        skimage.io.imsave(path, buffer)