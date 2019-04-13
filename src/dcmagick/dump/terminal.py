import numpy as np

from teimpy import Mode, get_drawer

from ..common.window import apply as apply_window


def _dump(mode, proxy):
    drawer = get_drawer(mode)
    return drawer.draw(apply_window(proxy))


def dump_braille(proxy):
    return _dump(Mode.BRAILLE, proxy)


def dump_halfblock(proxy):
    return _dump(Mode.HALF_BLOCK, proxy)


def dump_iterm2(proxy):
    return _dump(Mode.ITERM2_INLINE_IMAGE, proxy)
