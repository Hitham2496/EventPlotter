import pytest
import numpy as np
from EventPlotter import Particle, Event

p2 = Particle(2212, status=-1, px=0., py=0., pz=7.e+03, e=7e+03)

p1 = Particle(2212, status=-1, px=0., py=0., pz=7.e+03, e=7e+03)

A = Particle(21, status=-1, px=0., py=0., pz=1.0978691649e+02, e=1.0978691649e+02)

B = Particle(21, status=-1, px=0., py=0., pz=-4.9113387232e+01, e=4.9113387232e+01)

C = Particle(21, status=1, px=7.1902798158e+00, py=-6.7312608086e+01, pz=-4.440162797e-01, e=6.7697004968e+01, m=0.)

D = Particle(21, status=1, px=-7.1902798158e+00, py=+6.7312608086e+01, pz=-4.440162797e-01, e=6.7697004968e+01, m=0.)

E = Particle(21, status=1, px=3.0123136796e+01, py=7.05490777531e+01, pz=-1.3763091874e+02, e=1.5756536909e+02, m=0.)


event_balanced_beams = Event([p1, p2, A,B,C,D], 7000)
event_balanced = Event([A,B,C,D], 7000)
#event_unbalanced = Event([A,B,C,D,E], 7000)
#event_no_incoming = Event([C,D], 7000)


def test_momentum_balanced(event: Event):
    assert check_momentum(event) == True


def test_incoming(event: Event):
    # beams, incoming found, exceptions raised
    return


def test_set_info(event: Event, x_plus_true: float, x_minus_true: float):
    return



