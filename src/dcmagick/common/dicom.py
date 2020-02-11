from collections import namedtuple
from copy import deepcopy
from functools import singledispatch

import numpy as np
from pydicom.dataset import Dataset

from .. import __version__ as version
from . import uid
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


@singledispatch
def create_dataset_of(slice_proxy):
    import pdb

    pdb.set_trace()
    raise ValueError("Unknown slice proxy is given.")


@create_dataset_of.register(DicomSliceProxy)
def _d(slice_proxy):
    ds = deepcopy(slice_proxy.ref[0])
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
    return ds


@create_dataset_of.register(ImageSliceProxy)
def _i(slice_proxy):
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

    ds = Dataset()
    ds.file_meta = file_meta
    ds.preamble = b"\0" * 128
    ds.is_implicit_VR = True
    ds.is_little_endian = True
    ds.ImageType = ["ORIGINAL"]

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
    return ds


def _assign_pixel_data(ds, pixels):
    """
    Assign pixels and its information to dataset.

    >>> ds = Dataset()
    >>> _assign_pixel_data(ds, np.array([[0]], dtype=np.uint16))
    >>> assert ds.SamplesPerPixel == 1
    >>> assert ds.PhotometricInterpretation == "MONOCHROME1"
    >>> assert ds.BitsAllocated == 16
    >>> assert ds.BitsStored == 16
    >>> assert ds.HighBit == 15
    >>> assert ds.PixelRepresentation == 0
    >>> assert ds.Rows == 1
    >>> assert ds.Columns == 1
    >>> assert ds.PixelData == np.array([[0]], dtype=np.uint16).tobytes()
    """
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


def _get_pixel_info(pixels):
    """
    Get information about pixels.

    >>> _get_pixel_info(np.array([[0]], dtype=np.uint8))
    PixelInfo(samples_per_pixel=1, photometric_interpretation='MONOCHROME1', bits_allocated=8, pixel_representation=0)
    >>> _get_pixel_info(np.array([[[0, 0, 0]]], dtype=np.uint8))
    PixelInfo(samples_per_pixel=3, photometric_interpretation='RGB', bits_allocated=8, pixel_representation=0)
    >>> _get_pixel_info(np.array([[0]], dtype=np.uint16))
    PixelInfo(samples_per_pixel=1, photometric_interpretation='MONOCHROME1', bits_allocated=16, pixel_representation=0)
    >>> _get_pixel_info(np.array([[0]], dtype=np.int16))
    PixelInfo(samples_per_pixel=1, photometric_interpretation='MONOCHROME1', bits_allocated=16, pixel_representation=1)
    """
    samples_per_pixel = 3 if _is_rgb888(pixels) else 1
    photometric_interpretation = "RGB" if _is_rgb888(pixels) else "MONOCHROME1"
    bits_allocated = 8 * pixels.dtype.itemsize
    pixel_representation = 1 if pixels.dtype == np.int16 else 0

    return PixelInfo(
        samples_per_pixel,
        photometric_interpretation,
        bits_allocated,
        pixel_representation,
    )


def _is_rgb888(pixels):
    """
    Predicate function for RGB888 or not.

    >>> _is_rgb888(np.array([[[0, 0, 0]]], dtype=np.uint16))
    False
    >>> _is_rgb888(np.array([[[0, 0, 0]]], dtype=np.uint8))
    True
    >>> _is_rgb888(np.array([[0]]))
    False
    """

    is_rgb = pixels.ndim == 3 and pixels.shape[-1] == 3
    is_unit8 = pixels.dtype == np.uint8
    return is_rgb and is_unit8


def _is_mono(pixels):
    """
    Predicate function for monochrome or not.

    >>> _is_mono(np.array([[[0, 0, 0]]]))
    False
    >>> _is_mono(np.array([[0]]))
    True
    >>> _is_mono(np.array([[[0]]]))
    True
    """

    return pixels.ndim == 2 or (pixels.ndim == 3 and pixels.shape[-1] == 1)
