import pytest
import numpy as np
from EventPlotter import Particle

A = Particle(21, status=-1, px=0, py=0, pz=200, e=200)
B = Particle(21, status=-1, px=0, py=0, pz=-350, e=350)
C = Particle(21, status=1, px=0, py=0, pz=-150, e=550, m=529.15)

@pytest.mark.parametrize("part", [
    (A),
    (B),
    (C),
])
def test_on_shell(part: Particle):
    assert part.m_calc() == pytest.approx(part.m, Particle.TOL)


#@pytest.mark.parametrize("part", [
#    (A),
#    (B),
#    (C),
#])
#def test_off_shell(part: Particle):
#    with pytest.raises(ValueError):
#        part.check_on_shell()


@pytest.mark.parametrize("part", [
    (A),
    (B),
    (C),
])
def test_momentum_wrapper(part: Particle):

    assert part.e() == part.momentum.e
    assert part.px() == part.momentum.p_x
    assert part.py() == part.momentum.p_y
    assert part.pz() == part.momentum.p_z


@pytest.mark.parametrize("part, rap_control", [
    (A, np.inf),
    (B, -np.inf),
    (C, -0.5596),
])
def test_rapidity(part: Particle, rap_control: float):

    if (part.e() == part.pz()):
        assert np.abs(part.rap()) == np.inf

    if ( (part.e() + part.pz()) / (part.e() - part.pz()) ):
        with pytest.raises(ValueError):
            part.rap()

    assert part.rap() == pytest.approx(rap_control, Particle.TOL)


@pytest.mark.parametrize("part, perp_control", [
    (A, 0.),
    (B, 0.),
    (C, 0.),
])
def test_perp(part: Particle, perp_control: float):
    assert part.perp() == pytest.approx(perp_control, Particle.TOL)
