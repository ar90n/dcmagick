import numpy as np
from PIL import Image
from pydicom import dcmread

from .dicom import create_dataset_of
from .format import SliceFormat
from .proxy import DicomSliceProxy, ImageSliceProxy


def read(fo, input_params: dict = None, proxy_params: dict = None):
    _read_funcs = [_read_image, _read_dcm]

    input_params = {} if input_params is None else input_params
    proxy_params = {} if proxy_params is None else proxy_params
    for f in _read_funcs:
        try:
            return f(fo, input_params, proxy_params)
        except Exception:
            fo.seek(0)
    raise ValueError("Unknown format data is given.")


def _read_image(fo, input_params, src_params):
    img = Image.open(fo, **input_params)
    pixel_array = np.asarray(img)
    try:
        slice_format = SliceFormat(img.format)
    except ValueError:
        slice_format = SliceFormat.UNKNOWN
    return ImageSliceProxy(pixel_array, format=slice_format, params=src_params)


def _read_dcm(fo, input_params, src_params):
    dcmread_params = {
        k: src_params[k]
        for k in ["defer_size", "stop_before_pixels", "force", "specific_tags"]
        if k in src_params
    }
    dcm = dcmread(fo, **dcmread_params)
    return DicomSliceProxy(dcm, params=src_params)


def write(fo, slice_proxy, format=SliceFormat.UNKNOWN, params: dict = None):
    format = slice_proxy.ref[1] if format == SliceFormat.UNKNOWN else format
    params = {} if params is None else params

    if format == SliceFormat.DICOM:
        _write_dcm(fo, slice_proxy, params)
    elif format in [SliceFormat.JPEG, SliceFormat.PNG]:
        _write_image(fo, slice_proxy, format, params)
    else:
        raise ValueError(f"Unknown format({format}) is given.")


def _write_image(fo, slice_proxy, format, params):
    pixels = slice_proxy.pixels
    if pixels.dtype != np.uint8:
        min_value = float(np.min(pixels))
        max_value = float(np.max(pixels))
        pixels = (255 * (pixels - min_value) / (max_value - min_value)).astype(np.uint8)

    img = Image.fromarray(pixels)
    img.save(fo, format=format.value, **params)


def _write_dcm(fo, slice_proxy, params):
    ds = create_dataset_of(slice_proxy)
    ds.save_as(fo, **params)
