import numpy as np


def normalize_cast(arr, maxv=None, minv=None, dtype=None):
    maxv = np.max(arr) if maxv is None else maxv
    minv = np.min(arr) if minv is None else minv
    dtype = arr.dtype if dtype is None else dtype

    result = (arr - minv) / (maxv - minv)
    if issubclass(dtype.type, np.integer):
        result = np.round(np.iinfo(dtype).max * result)

    return result.astype(dtype)
