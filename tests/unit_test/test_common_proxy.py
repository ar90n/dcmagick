import numpy as np
import pytest
from pydicom import dcmread
from skimage.io import imread

from dcmagick.common.proxy import DicomSliceProxy, ImageSliceProxy


@pytest.fixture(
    params=[
        (
            "png_16x16_fo",
            imread,
            ImageSliceProxy,
            {},
            {
                "width": 16,
                "height": 16,
                "spacing": [np.nan, np.nan],
                "origin": [np.nan, np.nan, np.nan],
                "orientation": [[np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]],
            },
        ),
        (
            "dcm_16x16_le_fo",
            dcmread,
            DicomSliceProxy,
            {},
            {
                "width": 16,
                "height": 16,
                "spacing": [1.0, 1.0],
                "origin": [0, 0, 0],
                "orientation": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            },
        ),
        (
            "png_16x16_fo",
            imread,
            ImageSliceProxy,
            {
                "spacing": [1.0, 1.0],
                "origin": [0, 0, 0],
                "orientation": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            },
            {
                "width": 16,
                "height": 16,
                "spacing": [1.0, 1.0],
                "origin": [0, 0, 0],
                "orientation": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            },
        ),
    ]
)
def read_slice_proxy_context(request):
    fo = request.getfixturevalue(request.param[0])
    content = request.param[1](fo)
    return (content, *request.param[2:])


def test_read_slice_proxy(read_slice_proxy_context):
    content, ProxyClass, attrs, expects = read_slice_proxy_context
    proxy = ProxyClass(content, attrs=attrs)
    assert proxy.width == expects["width"]
    assert proxy.height == expects["height"]
    assert np.allclose(proxy.spacing, expects["spacing"], equal_nan=True)
    assert np.allclose(proxy.origin, expects["origin"], equal_nan=True)
    assert np.allclose(proxy.orientation, expects["orientation"], equal_nan=True)


@pytest.fixture(
    params=[
        ("png_16x16_fo", imread, ImageSliceProxy),
        ("dcm_16x16_le_fo", dcmread, DicomSliceProxy),
    ]
)
def write_slice_proxy_context(request):
    fo = request.getfixturevalue(request.param[0])
    content = request.param[1](fo)
    return (content, *request.param[2:])


def test_write_slice_proxy(write_slice_proxy_context):
    content, ProxyClass = write_slice_proxy_context
    proxy = ProxyClass(content, attrs={})

    proxy.pixels = np.arange(12).reshape(3, 4)
    assert proxy.width == 4
    assert proxy.height == 3

    proxy.spacing = np.array([1.0, 2.0])
    assert np.allclose(proxy.spacing, np.array([1.0, 2.0]))

    proxy.origin = np.array([1.0, 2.0, 3.0])
    assert np.allclose(proxy.origin, np.array([1.0, 2.0, 3.0]))

    proxy.orientation = np.arange(6).reshape(2, 3)
    assert np.allclose(proxy.orientation, np.arange(6).reshape(2, 3))


@pytest.fixture(
    params=[
        (
            "png_16x16_fo",
            imread,
            ImageSliceProxy,
            {
                "spacing": [1.0, 1.0],
                "origin": [0, 0, 0],
                "orientation": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
                "foo": 123,
            },
            None,
            {
                "spacing": [1.0, 1.0],
                "origin": [0, 0, 0],
                "orientation": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
                "foo": 123,
            },
        ),
        (
            "dcm_16x16_le_fo",
            dcmread,
            DicomSliceProxy,
            {
                "spacing": [2.0, 2.0],
                "origin": [1, 2, 3],
                "orientation": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
                "foo": 123,
            },
            None,
            {
                "spacing": [2.0, 2.0],
                "origin": [1, 2, 3],
                "orientation": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
                "foo": 123,
            },
        ),
        (
            "dcm_16x16_le_fo",
            dcmread,
            DicomSliceProxy,
            {
                "PixelSpacing": [2.0, 2.0],
                "ImagePositionPatient": [1.0, 2.0, 3.0],
                "ImageOrientationPatient": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
            },
            {
                "spacing": [2.0, 2.0],
                "origin": [1.0, 2.0, 3.0],
                "orientation": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
            },
            None,
        ),
        (
            "dcm_16x16_le_fo",
            dcmread,
            DicomSliceProxy,
            {
                "spacing": [2.0, 2.0],
                "origin": [1.0, 2.0, 3.0],
                "ImageOrientationPatient": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
            },
            {
                "PixelSpacing": [2.0, 2.0],
                "ImagePositionPatient": [1.0, 2.0, 3.0],
                "ImageOrientationPatient": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
            },
            {
                "spacing": [2.0, 2.0],
                "origin": [1.0, 2.0, 3.0],
                "orientation": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
            },
        ),
        (
            "dcm_16x16_le_fo",
            dcmread,
            DicomSliceProxy,
            {
                "PixelSpacing": [2.0, 2.0],
                "ImagePositionPatient": [1.0, 2.0, 3.0],
                "ImageOrientationPatient": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
            },
            {
                "PixelSpacing": [2.0, 2.0],
                "ImagePositionPatient": [1.0, 2.0, 3.0],
                "ImageOrientationPatient": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
            },
            {
                "spacing": [2.0, 2.0],
                "origin": [1.0, 2.0, 3.0],
                "orientation": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
            },
        ),
    ]
)
def modify_slice_proxy_context(request):
    fo = request.getfixturevalue(request.param[0])
    slice_proxy = request.param[2](request.param[1](fo))
    return (slice_proxy, *request.param[3:])


def test_modify_slice_proxy(modify_slice_proxy_context):
    slice_proxy, attrs, expect_attrs, expect_dict = modify_slice_proxy_context
    if expect_attrs is None:
        expect_attrs = attrs
    if expect_dict is None:
        expect_dict = expect_attrs

    for k, v in attrs.items():
        setattr(slice_proxy, k, v)

    for k, v in expect_attrs.items():
        assert np.all(getattr(slice_proxy, k) == v)

    actual_dict = {
        k: v for k, v in slice_proxy.__dict__.items() if not k.startswith("_")
    }
    assert actual_dict == expect_dict
