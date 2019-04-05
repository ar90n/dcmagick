import re
import sys
from contextlib import contextmanager

from . import io
from .format import SliceFormat, get_format
from .proxy import DicomSliceProxy, ImageSliceProxy


def _parse_dst_path(dst_path: str):
    """
    Parse given imagemagick like path to get format and destination path.
    >>> _parse_dst_path("png:output.dcm")
    (<SliceFormat.PNG: 'PNG'>, 'output.dcm')
    >>> _parse_dst_path("output.dcm")
    (<SliceFormat.DICOM: 'DICOM'>, 'output.dcm')
    >>> _parse_dst_path("output")
    (<SliceFormat.UNKNOWN: 'UNKNOWN'>, 'output')
    >>> _parse_dst_path("foo:output.dcm")
    Traceback (most recent call last):
      ...
    dcmagick.common.exception.NotSupportFormatError: foo is not supported.
    """
    m = re.match(r"^\s*([^:]*):(.*)$", dst_path)
    if m is not None:
        return get_format(m.group(1)), m.group(2)
    m = re.match(r"^\s*(.*)\.(.*)$", dst_path)
    if m is not None:
        return get_format(m.group(2)), dst_path
    return SliceFormat.UNKNOWN, dst_path


@contextmanager
def slice_context(src_path: str, dst_path: str, params: dict = None):
    params = {} if params is None else params
    src_fo = sys.stdin if src_path == "-" else open(src_path, "rb")
    try:
        slice_proxy = io.read(src_fo, **params.get("input", {}))
        yield slice_proxy, params.get("proc", {})

        if dst_path is not None:
            dst_format, real_dst_path = _parse_dst_path(dst_path)
            dst_fo = (
                sys.stdout.buffer if real_dst_path == "-" else open(real_dst_path, "wb")
            )
            try:
                io.write(dst_fo, slice_proxy, dst_format, **params.get("output", {}))
            finally:
                dst_fo.flush()
                if real_dst_path != "-":
                    dst_fo.close()
    finally:
        if src_path != "-":
            src_fo.close()
