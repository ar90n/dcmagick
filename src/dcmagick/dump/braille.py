import numpy as np

from teimpy import Mode, get_drawer


def dump_braille(proxy):
    drawer = get_drawer(Mode.BRAILLE)
    return drawer.draw(proxy.pixels.astype(np.int32))
