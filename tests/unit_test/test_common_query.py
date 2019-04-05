import pytest

from dcmagick.common import io, query


@pytest.fixture(
    params=[
        ("png_16x16_fo", {}, True),
        ("png_16x16_fo", {"width": 16, "height": 16}, True),
        ("png_16x16_fo", {"width": 16, "height": 17}, False),
        ("dcm_16x16_le_fo", {}, True),
        ("dcm_16x16_le_fo", {"width": 16, "height": 16, "Modality": "CT"}, True),
        ("dcm_16x16_le_fo", {"width": 16, "height": 17}, False),
    ]
)
def test_query_context(request):
    src_fixture, condition, expect = request.param
    fo = request.getfixturevalue(src_fixture)
    return (fo, condition, expect)


def test_query(test_query_context):
    fo, condition, expect = test_query_context
    proxy = io.read(fo)

    assert query.match(condition, proxy) == expect
