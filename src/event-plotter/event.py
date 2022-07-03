import particle.Particle as Particle
import numpy as np
import pylorentz


class Event():

    def __init__(
                 self, particles: np.ndarray[Particle], mur: float=0.,
                 muf: float=0., set_info: bool=True, root_s: float=0.,
                 x_plus: float=0., x_minus: float=0.
                ):
        """
        Saves information of particles in an event and sets
        additional information of event by default 
        """
        self.particles = particles
        self.mur = mur
        self.muf = muf
        if (set_info):
            self.setup()
            return

        self.root_s = root_s
        self.x_plus = x_plus
        self.x_minus = x_minus

    def setup(self):
        """
        Calculates global quantities of event including:
        centre of mass energy, pdf energy fractions.
        """

