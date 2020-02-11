from enum import Enum

from .exception import NotSupportFormatError


class SliceFormat(Enum):
    DICOM = "DICOM"
    JPEG = "JPEG"
    PNG = "PNG"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def of(cls, format: str):
        """
        Get SliceFormat of given string.

        >>> SliceFormat.of("dcm")
        <SliceFormat.DICOM: 'DICOM'>
        >>> SliceFormat.of("jpg")
        <SliceFormat.JPEG: 'JPEG'>
        >>> SliceFormat.of("jpeg")
        <SliceFormat.JPEG: 'JPEG'>
        >>> SliceFormat.of("png")
        <SliceFormat.PNG: 'PNG'>
        """

        if format in ["dcm"]:
            return SliceFormat.DICOM
        elif format in ["jpg", "jpeg"]:
            return SliceFormat.JPEG
        elif format in ["png"]:
            return SliceFormat.PNG
        raise NotSupportFormatError(f"Couldn't get format from {format}.")
