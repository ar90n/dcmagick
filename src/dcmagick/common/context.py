import re
import sys
from typing import Optional, IO
from contextlib import contextmanager

from . import io
from .format import SliceFormat
from .proxy import DicomSliceProxy, ImageSliceProxy


def _parse_dst_path(path: str):
    """
    Parse given imagemagick like path to get format and destination path.

    Parameters
    ----------
    path : str
        Imagemagick linke path such as format:path.

    >>> _parse_dst_path("png:output.dcm")
    (<SliceFormat.PNG: 'PNG'>, 'output.dcm')
    >>> _parse_dst_path("output.dcm")
    (<SliceFormat.DICOM: 'DICOM'>, 'output.dcm')
    >>> _parse_dst_path("output")
    (<SliceFormat.UNKNOWN: 'UNKNOWN'>, 'output')
    >>> _parse_dst_path("foo:output.dcm")
    Traceback (most recent call last):
      ...
    dcmagick.common.exception.NotSupportFormatError: Couldn't get format from foo.
    """
    m = re.match(r"^\s*([^:]*):(.*)$", path)
    if m is not None:
        return SliceFormat.of(m.group(1)), m.group(2)
    m = re.match(r"^\s*(.*)\.(.*)$", path)
    if m is not None:
        return SliceFormat.of(m.group(2)), path
    return SliceFormat.UNKNOWN, path


@contextmanager
def slice_context(src_path: str, dst_path: Optional[str], params: dict = None):
    """
    Slice-wise processing context

    Parameters
    ----------
    src_path : str
        String path to source file.
    dst_path : str
        Imagemagick like path to dstination file.
    params : dict
        Parameters to any features in context. This argument may takes the follwing keys.
        Values to each keys should be dict and contain any value.
            * input  : Parameters for input process such as file reading.
            * proxy  : Parameters for proxy object. This is used for overriding its attributes.
            * output : Parameters for output process such as file writing.
    """

    params = {} if params is None else params
    src_fo = sys.stdin if src_path == "-" else open(src_path, "rb")
    input_params = params.get("input", {})
    proxy_params = params.get("proxy", {})
    output_params = params.get("output", {})
    try:
        slice_proxy = io.read(
            src_fo, input_params=input_params, proxy_params=proxy_params
        )
        yield slice_proxy

        if dst_path is not None:
            dst_format, real_dst_path = _parse_dst_path(dst_path)
            dst_fo = (
                sys.stdout.buffer if real_dst_path == "-" else open(real_dst_path, "wb")
            )
            try:
                io.write(dst_fo, slice_proxy, dst_format, params=output_params)
            finally:
                dst_fo.flush()
                if real_dst_path != "-":
                    dst_fo.close()
    finally:
        if src_path != "-":
            src_fo.close()  # type: ignore
