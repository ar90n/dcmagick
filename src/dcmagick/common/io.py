from collections import namedtuple
from copy import deepcopy
from functools import singledispatch

import numpy as np
from PIL import Image
from pydicom import dcmread
from pydicom.dataset import Dataset

from .. import __version__ as version
from . import uid
from .format import SliceFormat
from .proxy import DicomSliceProxy, ImageSliceProxy

PixelInfo = namedtuple(
    "PixelInfo",
    [
        "samples_per_pixel",
        "photometric_interpretation",
        "bits_allocated",
        "pixel_representation",
    ],
)


def read(fo):
    _read_funcs = [_read_image, _read_dcm]

    for f in _read_funcs:
        try:
            return f(fo)
        except:
            fo.seek(0)
    raise ValueError("Unknown format data is given.")


def _read_image(fo, attrs=None):
    img = Image.open(fo)
    pixel_array = np.asarray(img)
    try:
        slice_format = SliceFormat(img.format)
    except ValueError:
        slice_format = SliceFormat.UNKNOWN
    return ImageSliceProxy(pixel_array, format=slice_format, attrs=attrs)


def _read_dcm(fo, attrs=None):
    dcm = dcmread(fo)
    return DicomSliceProxy(dcm, attrs=attrs)


def write(fo, slice_proxy, fmt=None, **params):
    fmt = slice_proxy.ref[1] if fmt is None else fmt
    if fmt == SliceFormat.DICOM:
        _write_dcm(fo, slice_proxy)
    elif fmt in [SliceFormat.JPEG, SliceFormat.PNG]:
        _write_image(fo, slice_proxy, fmt=fmt, **params)
    elif fmt == SliceFormat.UNKNOWN:
        _write_image(fo, slice_proxy, fmt=SliceFormat.PNG, **params)
    else:
        raise ValueError(f"Unknown format({fmt}) is given.")


def _write_image(fo, slice_proxy, fmt=SliceFormat.PNG, **params):
    img = Image.fromarray(slice_proxy.pixels)
    img.save(fo, fmt=fmt.value, **params)


def _is_rgb888(pixels):
    is_rgb = pixels.ndim == 3 and pixels.shape[-1] == 3
    is_unit8 = pixels.dtype == np.uint8
    return is_rgb and is_unit8


def _is_mono(pixels):
    return pixels.ndim == 2 or (pixels.ndim == 3 and pixels.shape[-1] == 1)


def _get_pixel_info(pixels):
    samples_per_pixel = 3 if _is_rgb888(pixels) else 1
    photometric_interpretation = "RGB" if _is_rgb888(pixels) else "MONOCHROME1"
    bits_allocated = 8 if _is_rgb888(pixels) else 16
    pixel_representation = 1 if pixels.dtype == np.int16 else 0

    return PixelInfo(
        samples_per_pixel,
        photometric_interpretation,
        bits_allocated,
        pixel_representation,
    )


def _assign_pixel_data(ds, pixels):
    if not _is_rgb888(pixels) and not _is_mono(pixels):
        raise ValueError("Given not supported pixel type.")

    ds.PixelData = pixels.tobytes()
    ds.Rows = pixels.shape[0]
    ds.Columns = pixels.shape[1]

    pixel_info = _get_pixel_info(pixels)
    ds.SamplesPerPixel = pixel_info.samples_per_pixel
    ds.PhotometricInterpretation = pixel_info.photometric_interpretation
    ds.BitsAllocated = pixel_info.bits_allocated
    ds.BitsStored = ds.BitsAllocated
    ds.HighBit = ds.BitsAllocated - 1
    ds.PixelRepresentation = pixel_info.pixel_representation


@singledispatch
def _create_dataset(slice_proxy):
    raise ValueError("Unknown slice proxy is given.")


@_create_dataset.register(DicomSliceProxy)
def _(slice_proxy):
    return deepcopy(slice_proxy.ref[0])


@_create_dataset.register(ImageSliceProxy)
def _(slice_proxy):
    sop_inst_uid = uid.generate_uid()

    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = (
        uid.storage_sopclass_uids.SecondaryCaptureImageStorage
    )
    file_meta.MediaStorageSOPInstanceUID = sop_inst_uid
    file_meta.ImplementationClassUID = uid.DCMAGICK_IMPLEMENTATION_UID
    file_meta.ImplementationVersionName = version
    file_meta.FileMetaInformationGroupLength = 0
    file_meta.FileMetaInformationVersion = b"\x00\x01"
    file_meta.TransferSyntaxUID = uid.ImplicitVRLittleEndian

    ds = Dataset({}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.is_implicit_VR = True
    ds.is_little_endian = True
    ds.ImageType = ["ORIGINAL"]

    pixels, _, _ = slice_proxy.ref
    _assign_pixel_data(ds, pixels)
    return ds


def _write_dcm(fo, slice_proxy):
    ds = _create_dataset(slice_proxy)

    for k, v in slice_proxy.__dict__.items():
        if k.startswith("_"):
            continue
        elif k == "pixels":
            _assign_pixel_data(ds, v)
        elif k == "spacing":
            ds.PixelSpacing = list(v)
        elif k == "origin":
            ds.ImagePositionPatient = list(v)
        elif k == "orientation":
            ds.ImageOrientationPatient = list(v.reshape(-1))
        else:
            setattr(ds, k, v)
    ds.save_as(fo)
