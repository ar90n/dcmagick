import numpy as np


def calc_window(pixel_array, *, wc=None, ww=None):
    minv = np.min(pixel_array)
    maxv = np.max(pixel_array)

    wc = (maxv + minv) // 2 if wc is None else wc
    ww = 2 * min(abs(minv - wc), abs(maxv - wc)) if ww is None else ww
    return wc, ww


def apply_linear_window(pixel_array, wc, ww):
    half_width = ww // 2
    minv = wc - half_width
    maxv = wc + half_width

    window_applied = pixel_array.copy()
    window_applied[pixel_array < minv] = minv
    window_applied[maxv < pixel_array] = maxv
    window_applied = 255.0 * (window_applied - minv) / (maxv - minv)
    window_applied = window_applied.astype(np.uint8)
    return window_applied
