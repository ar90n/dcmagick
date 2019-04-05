from abc import ABC, abstractproperty

import numpy as np

from .format import SliceFormat


class proxy_property:
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self

        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


class SliceProxy(ABC):
    def __init__(self, params=None):
        if params is not None:
            self.__dict__.update(params)

    @property
    def width(self):
        return self.pixels.shape[1]

    @property
    def height(self):
        return self.pixels.shape[0]

    @abstractproperty
    def pixels(self):
        raise NotImplementedError("pixels must be implemented.")

    @abstractproperty
    def spacing(self):
        raise NotImplementedError("spacing must be implemented.")

    @abstractproperty
    def origin(self):
        raise NotImplementedError("origin must be implemented.")

    @abstractproperty
    def orientation(self):
        raise NotImplementedError("orientation must be implemented.")

    @abstractproperty
    def ref(self):
        raise NotImplementedError("ref must be implemented.")


class ImageSliceProxy(SliceProxy):
    def __init__(self, pixel_array, format=None, params=None):
        super().__init__(params)
        self._pixel_array = pixel_array
        self._format = SliceFormat.UNKNOWN if format is None else format
        self._params = params

    @proxy_property
    def pixels(self):
        return self._pixel_array.copy()

    @proxy_property
    def spacing(self):
        return np.array([np.nan, np.nan])

    @proxy_property
    def origin(self):
        return np.array([np.nan, np.nan, np.nan])

    @proxy_property
    def orientation(self):
        return np.array([[np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]])

    @property
    def format(self):
        return self._format

    @property
    def ref(self):
        return (self._pixel_array, self._format, self._params)


class DicomSliceProxy(SliceProxy):

    _PROXY_KEY_MAP = {
        "PixelSpacing": "spacing",
        "ImagePositionPatient": "origin",
        "ImageOrientationPatient": "orientation",
    }

    def __init__(self, dcm, params=None):
        super().__init__(params)
        self._dcm = dcm
        self._params = params

    @proxy_property
    def pixels(self):
        if hasattr(self._dcm, "pixel_array"):
            return self._dcm.pixel_array.copy()
        return np.array([], shape=(0, 0))

    @proxy_property
    def spacing(self):
        if hasattr(self._dcm, "PixelSpacing"):
            return np.array(self._dcm.PixelSpacing)
        if hasattr(self._dcm, "ImagerPixelSpacing"):
            return self._dcm.ImagerPixelSpacing
        return np.array([np.nan, np.nan])

    @proxy_property
    def origin(self):
        if hasattr(self._dcm, "ImagePositionPatient"):
            return np.array(self._dcm.ImagePositionPatient)
        return np.array([np.nan, np.nan, np.nan])

    @proxy_property
    def orientation(self):
        if hasattr(self._dcm, "ImageOrientationPatient"):
            return np.array(self._dcm.ImageOrientationPatient).reshape(2, 3)
        return np.array([[np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]])

    @property
    def ref(self):
        return (self._dcm, SliceFormat.DICOM, self._params)

    def __getattr__(self, key):
        proxy_key = self._PROXY_KEY_MAP.get(key, key)
        if proxy_key != key:
            return getattr(self, proxy_key)

        if hasattr(self._dcm, key):
            value = self._dcm.get(key)
            self.__dict__[key] = value
            return value
        raise AttributeError(f"'DicomSliceProxy' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        key = self._PROXY_KEY_MAP.get(key, key)
        self.__dict__[key] = value
