"""
plot-event.py: example showing application of LHE reading methods
to produce 2D histogram plots with the Plotter class

The LHE file used may be found in the `test` directory.
"""
from EventPlotter import Particle, Event, Plotter, ReaderLHEF
import os

def energy_over_perp(particle):
    """
    Calculates energy of particle divided by its
    transverse momentum.

    :param particle: Particle to calculate scale for.
    """
    return particle.E()/particle.perp()
 

def main(filename):
    """
    Plot first three events in LHE file.

    :param filename: str name of LHE file including path.
    """
    plots = Plotter(rap_extent=[-4.5, 4.5], bins=50, chosen_map="cividis",
                    custom_z_axis=energy_over_perp, z_label=r"$E/p_\perp$",
                    include_wgt=True)

    events = ReaderLHEF(str(filename), wgt_idx=0)

    counter = 0
    for event in events:
        if counter == 3:
            break

        counter += 1
        img = plots.get_image(event)
        plots.plot_y_phi(img, title="event-"+str(counter)+".png")


if __name__ == """__main__""":
    os.system("gunzip ../test/HEJFOG.lhe.gz")
    main("../HEJFOG.lhe")
    os.system("gzip ../test/HEJFOG.lhe")
