import pytest
import os
from EventPlotter import Particle, Event, ReaderLHEF, Reader


init_info = [2212.0, 2212.0, 3500.0, 3500.0, 0.0, 0.0,
             303400.0, 303400.0, -3.0, 9.0]

def test_incorrect_ext():
    with pytest.raises(ValueError):
        reader = ReaderLHEF("test/HEJFOG.lhe.gz", wgt_idx=0)


def test_reading():
    os.system("gunzip test/HEJFOG.lhe.gz")
    reader = ReaderLHEF("test/HEJFOG.lhe", wgt_idx=0)
    assert reader.init_info == init_info
    for idx, ev in enumerate(reader):
        assert isinstance(ev, Event)

    os.system("gzip test/HEJFOG.lhe")
