from dcmagick.common.context import slice_context
from dcmagick.common import io
import numpy as np


def test_context(jpg_16x16_path, tmpdir):
    dst_path = tmpdir / "dst"
    with slice_context(
        str(jpg_16x16_path), str(dst_path), io.SliceFormat.JPEG
    ) as proxy:
        assert proxy.width == 16
        proxy.pixels = np.arange(100).reshape(10, 10)
