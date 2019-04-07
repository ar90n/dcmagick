import numpy as np

from teimpy import Mode, get_drawer

from ..common.improc import normalize_cast


def _dump(mode, proxy):
    drawer = get_drawer(mode)
    return drawer.draw(normalize_cast(proxy.pixels, np.dtype("uint8")))


def dump_braille(proxy):
    return _dump(Mode.BRAILLE, proxy)


def dump_halfblock(proxy):
    return _dump(Mode.HALF_BLOCK, proxy)


def dump_iterm2(proxy):
    return _dump(Mode.ITERM2, proxy)
