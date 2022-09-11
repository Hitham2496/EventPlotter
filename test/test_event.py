import pytest
import numpy as np
from EventPlotter import Particle, Event

A = Particle(21, status=-1, px=0, py=0, pz=200, e=200)

B = Particle(21, status=-1, px=0, py=0, pz=-350, e=350)

C = Particle(21, status=1, px=7.1902798158e+00, py=-6.7312608086e+01, pz=-4.440162797e-01, e=6.7697004968e+01, m=0.)

D = Particle(21, status=1, px=-7.1902798158e+00, py=+6.7312608086e+01, pz=-4.440162797e-01, e=6.7697004968e+01, m=0.)

E = Particle(21, status=1, px=3.0123136796e+01, py=7.05490777531e+01, pz=-1.3763091874e+02, e=1.5756536909e+02, m=0.)


event_balanced = Event([A,B,C,D], 7000)
event_unbalanced = Event([A,B,C,D,E], 7000)
