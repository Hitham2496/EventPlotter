import pytest
import numpy as np
import pylorentz
from EventPlotter import Particle

A = Particle(21, status=-1, px=0, py=0, pz=200, e=200)

B = Particle(12, status=-1, px=0, py=0, pz=-350, e=350)

C = Particle(1, status=1, px=0, py=0, pz=-150, e=550, m=529.15)

D = Particle(22, status=1, px=-2.026831e+01, py=-1.871849e+01,
             pz=-1.510034e+02, e=1.535032e+02, m=0.139)

E = Particle(-11, status=1, px=-6.838323e+00, py=-3.602227e+02, 
             pz=1.114048e+02, e=3.771183e+02, m=0.167) 


@pytest.mark.parametrize("part", [
    (A),
    (B),
    (C),
    (D),
    (E),
])
def test_on_shell(part: Particle):
    assert part.m_calc() == pytest.approx(part.m, Particle.TOL)


@pytest.mark.parametrize("part, out_status, is_parton", [
    (A, False, True),
    (B, False, False),
    (C, True, True),
    (D, True, False),
])
def test_metadata(part: Particle, out_status: bool, is_parton: bool):
    assert part.is_final() == out_status
    assert part.is_incoming() is not (part.is_final())
    assert part.is_parton() == is_parton


def test_off_shell():
    # Test wrong masses
    with pytest.raises(ValueError):
        F = Particle(-24, status=1, px=-6.838323e+00, py=-3.602227e+02, 
                     pz=1.114048e+02, e=3.771183e+02, m=68.432)

    with pytest.raises(ValueError):
        G = Particle(21, status=1, px=0, py=0, pz=-150, e=550, m=29.15) 

    # Test momentum outside of tolerance for zero mass
    with pytest.raises(ValueError):
        H = Particle(-21, status=1, px=-6.838323e+00, py=-3.602227e+02, 
                     pz=1.114048e+02, e=3.871183e+02, m=0.)

    # Test negative mass input
    with pytest.raises(ValueError):
        I = Particle(-21, status=1, px=-6.838323e+00, py=-3.602227e+02, 
                     pz=1.114048e+02, e=3.871183e+02, m=-10.)


@pytest.mark.parametrize("part", [
    (A),
    (B),
    (C),
    (D),
    (E),
])
def test_momentum_wrapper(part: Particle):

    p = part.momentum
    assert isinstance(p, pylorentz.Momentum4)
    assert part.e() == p.e
    assert part.px() == p.p_x
    assert part.py() == p.p_y
    assert part.pz() == p.p_z
    assert part.phi() == p.phi


@pytest.mark.parametrize("part, rap_control", [
    (A, np.inf),
    (B, -np.inf),
    (C, -0.27980),
    (D, -2.4013),
    (E, 0.3045),
])
def test_rapidity(part: Particle, rap_control: float):

    if (part.e() == part.pz()):
        assert part.rap() == np.inf

    if (part.e() == -part.pz()):
        assert part.rap() == -np.inf

    assert part.rap() == pytest.approx(rap_control, Particle.TOL)


@pytest.mark.parametrize("part, perp_control", [
    (A, 0.),
    (B, 0.),
    (C, 0.),
    (D, 27.58960),
    (E, 360.2649),
])
def test_perp(part: Particle, perp_control: float):
    assert part.perp() == pytest.approx(perp_control, Particle.TOL)
