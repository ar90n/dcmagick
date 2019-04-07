import numpy as np


def normalize_cast(arr, dtype):
    maxv = np.max(arr)
    minv = np.min(arr)
    result = (arr - minv) / (maxv - minv)
    if issubclass(dtype.type, np.integer):
        result = np.round(np.iinfo(dtype).max * result)

    return result.astype(dtype)

