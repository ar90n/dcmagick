import pickle
import sys
from pathlib import Path

import pytest

src_root_path = (Path(__file__).parent.parent / "src").absolute()
sys.path.append(str(src_root_path))

DATA_ROOT = Path(__file__).parent / "data"
data_root_path = pytest.fixture()(DATA_ROOT.absolute)


def generage_pickle_fixture(filename):
    pickle_path = DATA_ROOT / filename

    def _f():
        with pickle_path.open("rb") as f_pickle:
            yield pickle.load(f_pickle)

    return pytest.fixture(scope="function")(_f)


def generage_data_access_fixture(filename):
    data_path = (DATA_ROOT / filename).absolute()

    def _f():
        with data_path.open("rb") as f_data:
            yield f_data

    fixture = pytest.fixture(scope="function")
    return fixture(_f), fixture(lambda: data_path)


expect_16x16 = generage_pickle_fixture("test_16x16.pickle")
jpg_16x16_fo, jpg_16x16_path = generage_data_access_fixture("test_16x16.jpg")
png_16x16_fo, png_16x16_path = generage_data_access_fixture("test_16x16.png")
dcm_16x16_le_fo, dcm_16x16_le_path = generage_data_access_fixture("test_16x16_le.dcm")
