import pytest
import numpy as np
from dcmagick.common import io
from dcmagick.common.format import SliceFormat
from dcmagick.common.proxy import ImageSliceProxy, DicomSliceProxy


@pytest.fixture(
    params=[
        ("png_16x16_fo", ImageSliceProxy, 0),
        ("jpg_16x16_fo", ImageSliceProxy, 10),
        ("dcm_16x16_le_fo", DicomSliceProxy, 0),
    ]
)
def read_context(request):
    fixture_value = request.getfixturevalue(request.param[0])
    return (fixture_value, *request.param[1:])


def test_read(read_context, expect_16x16):
    fo, expect_proxy_class, atol = read_context
    slice_proxy = io.read(fo)

    assert isinstance(slice_proxy, expect_proxy_class)
    assert np.allclose(slice_proxy.pixels, expect_16x16, atol=atol)


@pytest.fixture(params=[("png_16x16_fo",), ("jpg_16x16_fo",), ("dcm_16x16_le_fo",)])
def write_context(request):
    fo = request.getfixturevalue(request.param[0])
    slice_proxy = io.read(fo)
    return (slice_proxy,)


def test_write(write_context, tmpdir):
    slice_proxy = write_context[0]
    output_path = tmpdir / "output"

    with output_path.open("wb") as output_fo:
        slice_proxy.spacing = [2.3, 5.6]
        slice_proxy.Modality = 'DX'
        io.write(output_fo, slice_proxy, format=SliceFormat.DICOM)

    assert output_path.exists()
