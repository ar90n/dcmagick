import sys
from contextlib import contextmanager
from . import io
from .proxy import ImageSliceProxy, DicomSliceProxy


@contextmanager
def slice_context(src_path: str, dst_path: str, dst_format: io.SliceFormat):
    src_fo = sys.stdin if src_path == "-" else open(src_path, "rb")
    try:
        slice_proxy = io.read(src_fo)
        assert slice_proxy.width == 16
        yield slice_proxy
        assert slice_proxy.width == 10
    finally:
        if src_path != "-":
            src_fo.close()
