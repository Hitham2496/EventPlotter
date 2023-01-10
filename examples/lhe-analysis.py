"""
lhe-analysis.py: example showing application of LHE reading methods
to produce 1D histograms with matplotlib.

To use, unzip the sample LHE file in the test directory.
"""
from EventPlotter import Particle, Event, ReaderLHEF
import numpy as np
import matplotlib.pyplot as plt
import os


def H_T(event):
    """
    Calculates the scalar sum of transverse momenta in the final
    state of an event.

    :param event: event for which to calculate
    """
    ht = 0.
    for part in event:
        if part.is_final():
            ht += part.perp()
    return ht


def main(filename):
    """
    Implement an analysis of the H_T distribution of a sample
    of events in the LHE format.

    :param filename: str name of LHE file including path.
    """
    reading = ReaderLHEF(str(filename), wgt_idx=0)
 
    bins = np.linspace(0, 1000, 25)
    data = bins*0.

    for ev in reading:
       x = H_T(ev)
       for j, edge in enumerate(bins):
           if edge > x:
                data[j] += ev.wgt
                break

    data /= np.sum(data)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.xlabel(r"$H_T$ [GeV]")
    plt.ylabel(r"$d\sigma/dH_T$ [pb/GeV]")

    plt.step(bins, data, where="pre")
    plt.show()
    plt.clf()


if __name__ == """__main__""":
    os.system("gunzip ../test/HEJFOG.lhe.gz")
    main("../test/HEJFOG.lhe")
    os.system("gzip ../test/HEJFOG.lhe")
