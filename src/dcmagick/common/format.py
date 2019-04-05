from enum import Enum

from .exception import NotSupportFormatError


class SliceFormat(Enum):
    DICOM = "DICOM"
    JPEG = "JPEG"
    PNG = "PNG"
    UNKNOWN = "UNKNOWN"


def get_format(fmt: str):
    if fmt in ["dcm"]:
        return SliceFormat.DICOM
    elif fmt in ["jpg", "jpeg"]:
        return SliceFormat.JPEG
    elif fmt in ["png"]:
        return SliceFormat.PNG
    raise NotSupportFormatError(f"{fmt} is not supported.")
