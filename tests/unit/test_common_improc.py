import numpy as np
import pytest

from dcmagick.common import improc


@pytest.mark.parametrize(
    "input, expect",
    [
        (
            np.array([1.0, 1.5, 2.0], dtype=np.float32),
            np.array([0, 128, 255], dtype=np.uint8),
        ),
        (
            np.array([1.0, 1.5, 2.0], dtype=np.float32),
            np.array([0, 32768, 65535], dtype=np.uint16),
        ),
        (
            np.array([1, 2, 3], dtype=np.uint8),
            np.array([0, 0.5, 1.0], dtype=np.float32),
        ),
    ],
)
def test_normalize_cast(input, expect):
    assert np.allclose(improc.normalize_cast(input, dtype=expect.dtype), expect)
