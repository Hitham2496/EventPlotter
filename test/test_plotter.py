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

plots_invalid_func = Plotter(rap_extent=[-4.5, 4.5], bins=50, chosen_map="cividis",
                             custom_z_axis=lambda part: "bad return value",
                             z_label=r"$E/p_\perp$", include_wgt=True)

plots_invalid_func_prod = Plotter(rap_extent=[-4.5, 4.5], bins=50, chosen_map="cividis",
                                  custom_z_axis=lambda part: 0. if (part.pdg != 11) else "x",
                                  z_label=r"$E/p_\perp$", include_wgt=True)


def test_init__errors():
    # test inappropriate types for extents
    with pytest.raises(TypeError):
        plotting_invalid_rap = Plotter(rap_extent=4.5)
    with pytest.raises(TypeError):
        plotting_invalid_rap = Plotter(rap_extent=[4.5, 3.2, 2.1])
    with pytest.raises(TypeError):
        plotting_invalid_rap = Plotter(rap_extent=[4.5, "test"])
    with pytest.raises(TypeError):
        plotting_invalid_phi = Plotter(phi_extent=3.1)
    with pytest.raises(TypeError):
        plotting_invalid_phi = Plotter(phi_extent=[6.4, -3.2, 2.1])
    with pytest.raises(TypeError):
        plotting_invalid_phi = Plotter(phi_extent=[2.4, "test"])

    # test value error for |phi| > pi
    with pytest.raises(ValueError):
        plotting_invalid_phi = Plotter(phi_extent=[-4, 4])

    # test inappropriate bins
    with pytest.raises(TypeError):
        plotting_invalid_bins = Plotter(bins="test")
    with pytest.raises(ValueError):
        plotting_invalid_bins = Plotter(bins=-12)

    # test value error for min_val
    with pytest.raises(ValueError):
        plotting_invalid_phi = Plotter(min_val=-10)

    # test inappropriate colormap string
    with pytest.raises(TypeError):
        plotting_invalid_bins = Plotter(chosen_map=6)

    # test inappropriate z label string
    with pytest.raises(TypeError):
        plotting_invalid_bins = Plotter(z_label=4)

    # test inappropriate include_wgt
    with pytest.raises(TypeError):
        plotting_invalid_bins = Plotter(include_wgt="True")


def test_get_image():

    image, products = plots.get_image(event_balanced_beams, [7,8])
    image_no_products = plots.get_image(event_balanced_beams)
    image_no_beams = plots.get_image(event_balanced)

    # check the image output with/without beams/products is the same
    assert np.array_equal(image, image_no_products)
    assert np.array_equal(image, image_no_beams)

    # check the image shape and the length of the products list
    assert image.shape == (50, 50)
    assert isinstance(products, list)
    assert len(products) == 2

    # check type error is raised for invalid z function values
    with pytest.raises(TypeError):
        image_invalid = plots_invalid_func.get_image(event_balanced)
    with pytest.raises(TypeError):
        image_invalid = plots_invalid_func.get_image(event_balanced, [5, 6])

    # check for an invalid z function that affects only the products
    with pytest.raises(TypeError):
        image_invalid = plots_invalid_func_prod.get_image(event_balanced, [5, 6])

    # check value error is raised when image is not provided for plotting
    with pytest.raises(ValueError):
        image_invalid = plots.plot_y_phi()

    plots.plot_y_phi(image, products)
    plots.plot_y_phi(image_no_products)

