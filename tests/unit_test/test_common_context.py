import os
from io import BytesIO

import numpy as np
import pytest

from dcmagick.common import io
from dcmagick.common.context import slice_context


@pytest.fixture(
    params=[
        ("png_16x16_path", None, None),
        ("png_16x16_path", None, "dcm"),
        ("png_16x16_path", "dcm", None),
        ("jpg_16x16_path", None, None),
        ("jpg_16x16_path", None, "dcm"),
        ("jpg_16x16_path", "dcm", None),
        ("dcm_16x16_le_path", None, None),
        ("dcm_16x16_le_path", None, "dcm"),
        ("dcm_16x16_le_path", "dcm", None),
        ("dcm_16x16_le_path", None, "png"),
        ("dcm_16x16_le_path", "png", None),
        ("dcm_16x16_le_path", "png", "dcm"),
    ]
)
def test_convert_format_context(request, tmpdir):
    src_fixture, format, suffix = request.param
    format = "" if format is None else f"{format}:"
    suffix = "" if suffix is None else f".{suffix}"

    src_path = str(request.getfixturevalue(src_fixture))
    expect_dst_path = "{}/output{}".format(str(tmpdir), suffix)
    dst_path = "{}{}".format(format, expect_dst_path)
    return src_path, dst_path, expect_dst_path


def test_convert_format(test_convert_format_context):
    src_path, dst_path, expect_dst_path = test_convert_format_context
    expect_pixels = np.arange(100).reshape(10, 10).astype(np.uint8)

    with slice_context(src_path, dst_path) as proxy_and_params:
        proxy, proc_params = proxy_and_params
        assert proxy.width == 16
        assert proxy.height == 16
        proxy.pixels = expect_pixels

    assert os.path.exists(expect_dst_path)
    with open(expect_dst_path, "rb") as dst_fo:
        result = io.read(dst_fo)
        assert result.width == 10
        assert result.height == 10
        assert np.allclose(result.pixels, expect_pixels, atol=1)


@pytest.fixture(
    params=[("png_16x16_path",), ("jpg_16x16_path",), ("dcm_16x16_le_path",)]
)
def test_attr_override_context(request, tmpdir):
    src_fixture = request.param[0]

    src_path = str(request.getfixturevalue(src_fixture))
    dst_path = str(tmpdir / "output.dcm")
    expect_params = {
        "input": {
            "spacing": np.array([2.0, 3.0]),
            "origin": np.array([2.0, 3.0, 4.0]),
            "orientation": np.array([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]]),
            "Modality": "MR",
        },
        "proc": {"foo": 123},
        "output": {},
    }
    return src_path, dst_path, expect_params


def test_attr_override(test_attr_override_context):
    src_path, dst_path, expect_params = test_attr_override_context

    with slice_context(src_path, dst_path, expect_params) as proxy_and_params:
        proxy, proc_params = proxy_and_params
        assert proc_params == expect_params["proc"]
        assert np.allclose(proxy.spacing, expect_params["input"]["spacing"])
        assert np.allclose(proxy.origin, expect_params["input"]["origin"])
        assert np.allclose(proxy.orientation, expect_params["input"]["orientation"])

    assert os.path.exists(dst_path)
    with open(dst_path, "rb") as dst_fo:
        result = io.read(dst_fo)
        assert np.allclose(result.spacing, expect_params["input"]["spacing"])
        assert np.allclose(result.origin, expect_params["input"]["origin"])
        assert np.allclose(result.orientation, expect_params["input"]["orientation"])
        assert result.Modality == expect_params["input"]["Modality"]


def test_only_src(dcm_16x16_le_path):
    src_path = dcm_16x16_le_path

    with slice_context(src_path, None) as proxy_and_params:
        proxy, _ = proxy_and_params
        assert proxy.width == 16
        assert proxy.height == 16


def test_stdout(dcm_16x16_le_path, capfdbinary):
    src_path = dcm_16x16_le_path

    with slice_context(src_path, "-"):
        pass

    captured = capfdbinary.readouterr()
    slice_proxy = io.read(BytesIO(captured.out))
    assert slice_proxy.width == 16
    assert slice_proxy.height == 16


def test_stdin(dcm_16x16_le_fo, monkeypatch):
    monkeypatch.setattr("sys.stdin", dcm_16x16_le_fo)

    with slice_context("-", None) as proxy_and_params:
        slice_proxy, _ = proxy_and_params
        assert slice_proxy.width == 16
        assert slice_proxy.height == 16
