import re
from collections import Sequence

import numpy as np

from .exception import WindowFormatError
from .improc import normalize_cast
from .proxy import DicomSliceProxy, SliceProxy


def _parse_window(window: str, slice_proxy: SliceProxy):
    """
    Parse given window string.

    >>> from .proxy import ImageSliceProxy
    >>> proxy = ImageSliceProxy([[10, 50]])
    >>> _parse_window("100x200", proxy)
    (100.0, 200.0)
    >>> _parse_window("100x200abc", proxy)
    Traceback (most recent call last):
    ...
    dcmagick.common.exception.WindowFormatError: 100x200abc is invalid for --window.
    >>> _parse_window("0", proxy)
    (None, None)
    >>> proxy.WindowCenter = [200, 500]
    >>> proxy.WindowWidth = [300, 800]
    >>> _parse_window("0", proxy)
    (200.0, 300.0)
    >>> _parse_window("1", proxy)
    (500.0, 800.0)
    >>> _parse_window("2", proxy)
    (None, None)
    >>> proxy.WindowCenter = 200
    >>> proxy.WindowWidth = 300
    >>> _parse_window("0", proxy)
    (200.0, 300.0)
    >>> _parse_window("1", proxy)
    (None, None)
    >>> _parse_window(None, proxy)
    (30.0, 20.0)
    """
    if window is None:
        maxv = np.max(slice_proxy.pixels)
        minv = np.min(slice_proxy.pixels)
        wc = (maxv + minv) / 2
        ww = (maxv - minv) / 2
        return wc, ww

    m = re.match(r"^(\d+)$", window)
    if m is not None:
        index = int(m.group(1))
        wc_candidates = getattr(slice_proxy, "WindowCenter", [])
        if not isinstance(wc_candidates, Sequence):
            wc_candidates = [wc_candidates]
        wc = float(wc_candidates[index]) if index < len(wc_candidates) else None

        ww_candidates = getattr(slice_proxy, "WindowWidth", [])
        if not isinstance(ww_candidates, Sequence):
            ww_candidates = [ww_candidates]
        ww = float(ww_candidates[index]) if index < len(ww_candidates) else None
        return wc, ww

    m = re.match(r"^(\d+)x(\d+)$", window)
    if m is not None:
        wc = float(m.group(1))
        ww = float(m.group(2))
        return wc, ww

    raise WindowFormatError(f"{window} is invalid for --window.")


def assign(slice_proxy: SliceProxy, window: str):
    wc, ww = _parse_window(window, slice_proxy)
    if isinstance(slice_proxy, DicomSliceProxy) and (wc is None or ww is None):
        return

    setattr(slice_proxy, "WindowCenter", wc)
    setattr(slice_proxy, "WindowWidth", ww)


def apply(slice_proxy: SliceProxy) -> np.ndarray:
    wc = getattr(slice_proxy, "WindowCenter")
    wc = wc[0] if isinstance(wc, Sequence) else wc
    ww = getattr(slice_proxy, "WindowWidth")
    ww = ww[0] if isinstance(ww, Sequence) else ww

    if wc is None or ww is None:
        return normalize_cast(slice_proxy.pixels, dtype=np.dtype("uint8"))

    half_ww = ww // 2
    minv = wc - half_ww
    maxv = wc + half_ww
    windowed = np.clip(slice_proxy.pixels, minv, maxv)
    return normalize_cast(windowed, maxv=maxv, minv=minv, dtype=np.dtype("uint8"))
