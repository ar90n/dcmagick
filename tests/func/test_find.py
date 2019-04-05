import json

import pytest
from click.testing import CliRunner

from dcmagick.find import find


@pytest.fixture(
    params=[
        ("*.dcm", {"width": 16, "height": 16, "Modality": "CT"}, ["test_16x16_le.dcm"])
    ]
)
def test_find_context(request, data_root_path):
    name, query, expect_paths = request.param

    expect = "\n".join([str(data_root_path / p) for p in expect_paths]) + "\n"
    return data_root_path, name, query, expect


def test_find(test_find_context):
    root, name, query, expect = test_find_context

    args = []
    if name is not None:
        args.extend(["--name", name])
    if query is not None:
        args.extend(["--query", json.dumps(query)])
    args.append(str(root))

    runner = CliRunner()
    result = runner.invoke(find, args)
    assert result.exit_code == 0
    assert result.output == expect
