from scrambleverse.vrm import VRMReader
import os
from tempfile import NamedTemporaryFile


def test_open_vrm1():
    with VRMReader.open_file(os.environ["TEST_VRM1"]) as vrm:
        assert vrm.header.magic == b"glTF"
        assert vrm.header.version == 2
        assert vrm.vrm0meta is None
        assert vrm.vrm1meta is not None
        assert vrm.thumbnail is not None


def test_open_vrm1_tempfile():
    with open(os.environ["TEST_VRM1"], "rb") as f:
        filename = None
        try:
            with NamedTemporaryFile(
                suffix=".vrm",
                delete=False,
            ) as tmp:
                filename = tmp.name
                tmp.write(f.read())
                tmp.flush()
            with VRMReader.open_file(filename) as vrm:
                assert vrm.header.magic == b"glTF"
                assert vrm.header.version == 2
                assert vrm.vrm0meta is None
                assert vrm.vrm1meta is not None
                assert vrm.thumbnail is not None
        finally:
            if filename and os.path.exists(filename):
                os.remove(filename)
