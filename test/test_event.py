import pytest
from EventPlotter import Particle, Event


p1 = Particle(2212, status=-1, px=0., py=0., pz=3.5e+03, e=3.5e+03)
p2 = Particle(2212, status=-1, px=0., py=0., pz=-3.5e+03, e=3.5e+03)
A = Particle(3, status=-1, px=0., py=0., pz=80.387, e=80.387)
B = Particle(1, status=-1, px=0., py=0., pz=-435.476, e=435.476)
C = Particle(2, status=1, px=125.233, py=40.134, pz=-315.891, e=342.17125, m=0.)
D = Particle(21, status=1, px=-0.469, py=1.953, pz=-4.284, e=4.731, m=0.)
E = Particle(3, status=1, px=-52.286, py=-22.262, pz=-5.853, e=57.129, m=0.206)
F = Particle(-12, status=1, px=-65.701, py=-41.757, pz=-38.699, e=86.936, m=0.11)
G = Particle(11, status=1, px=-6.777, py=21.931, pz=9.638, e=24.896, m=0.15)

event_balanced_beams = Event([p1, p2, A, B, C, D, E, F, G], 7000)
event_balanced_info = Event([p1, p2, A, B, C, D, E, F, G], 7000, set_info=False,
                            x_plus=0.02297, x_minus=0.1244)
event_balanced = Event([A, B, C, D, E, F, G], 7000)


@pytest.mark.parametrize("event", [
    (event_balanced_beams),
    (event_balanced),
])
def test_momentum_balanced(event: Event):
    assert event.check_momentum()
    assert isinstance(str(event), str)


def test_momentum_val_error():
    with pytest.raises(ValueError):
        event_unbalanced = Event([A, B, C, D, E], 7000)  # noqa: F841

    with pytest.raises(ValueError):
        event_unbalanced = Event([p2, p1, C, D, E], 7000)  # noqa: F841


def test_reorder():
    # check reordering event is valid
    event_reorder = Event([p1, p2, B, C, A, D, E, F, G], 7000)
    event_reorder_beams = Event([p2, p1, B, C, A, D, E, F, G], 7000)
    assert event_reorder.check_momentum()
    assert event_reorder_beams.check_momentum()


def test_incoming():

    C_in = Particle(2, status=-1, px=125.233, py=40.134, pz=-315.891, e=342.17125, m=0.)
    D_in = Particle(21, status=-1, px=-0.469, py=1.953, pz=-4.284, e=4.731, m=0.)
    # test value error is raised for transverse incoming particles
    with pytest.raises(ValueError):
        ev_inc_only = Event([C_in, D_in, C, D], 7000.)  # noqa: F841
