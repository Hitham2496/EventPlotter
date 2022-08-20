"""

"""
from EventPlotter import particle
from EventPlotter import event


class Reader():

    def __enter__(self, filename: str):
        """
        Initialises an event reader object from the event file `filename`.
        """
        self.event_buffer = open(filename, 'r')

    def read_next(self, verbose: bool = False):
        """
        Advances the reader by one event.
        """

    def __exit__(self):
        """
        Closes the event file buffer on destruction.
        """
        self.event_buffer.close()


class ReaderLHEF(Reader):

    def read_next(self, verbose: bool = False):


class ReaderPythia(Reader):

    def read_next(self, verbose: bool = False):
#        particles = []
#        with open(file_in) as fstream:
#            for x in fstream.readlines():
#                if (len(x) > 2 and x[-2] != "-"):
#                    info = x.split()
#                    if (info[0] != "no" and info[0] != "Charge"):
#                        tmp = particle.Particle(int(info[1]), int(info[3]),
#                                                (int(info[4]), int(info[5])),
#                                                (int(info[6]), int(info[7])),
#                                                (int(info[8]), int(info[9])),
#                                                float(info[10]), float(info[11]),
#                                                float(info[12]), float(info[13]),
#                                                float(info[14]))
#                        particles.append(tmp)
#
#        if (verbose):
#            for idx, p in enumerate(particles):
#                print(idx, p.pdg, p.status, p.mothers, p.daughters, p.cols,
#                      p.momentum, p.m)
#
#        return event.Event(particles, 7000)
