from enum import Enum

from .exception import NotSupportFormatError


class SliceFormat(Enum):
    DICOM = "DICOM"
    JPEG = "JPEG"
    PNG = "PNG"
    UNKNOWN = "UNKNOWN"


def get_format(format: str):
    if format in ["dcm"]:
        return SliceFormat.DICOM
    elif format in ["jpg", "jpeg"]:
        return SliceFormat.JPEG
    elif format in ["png"]:
        return SliceFormat.PNG
    raise NotSupportFormatError(f"{format} is not supported.")
