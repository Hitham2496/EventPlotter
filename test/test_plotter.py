import pytest
import numpy as np
from EventPlotter import Particle, Event, Plotter
import sys
np.set_printoptions(threshold=sys.maxsize)


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
event_balanced = Event([A, B, C, D, E, F, G], 7000)

plots = Plotter(rap_extent=[-4.5, 4.5], bins=50, chosen_map="cividis",
                custom_z_axis=lambda part: part.e(),
                z_label=r"$E/p_\perp$", include_wgt=True)

def test_get_image():

    image, products = plots.get_image(event_balanced_beams, [7,8])
    image_no_products = plots.get_image(event_balanced_beams)

    assert type(image) == np.ndarray
    assert image.shape == (50, 50)
    assert len(products) == 2
    assert type(products) == list

    for part in products:
        assert type(part) == Particle

#print(products)

#plots.plot_y_phi(image, products)
#plots.plot_y_phi(image_no_products)

