import pytest
import os
from EventPlotter import Particle, Event, ReaderLHEF, Reader


init_info = [2212.0, 2212.0, 3500.0, 3500.0, 0.0, 0.0,
             303400.0, 303400.0, -3.0, 9.0]

def test_incorrect_ext():
    with pytest.raises(ValueError):
        reader = ReaderLHEF("HEJFOG.lhe.gz", wgt_idx=0)


def test_reading():
    os.system("gunzip HEJFOG.lhe.gz")
    reader = ReaderLHEF("HEJFOG.lhe", wgt_idx=0)
    assert reader.init_info == init_info
    for idx, ev in enumerate(reader):
        assert isinstance(ev, Event)



 #   iter_ev = iter(reader)

    os.system("gzip HEJFOG.lhe")
