#!/usr/bin/env python
"""
Particle class definition
"""
import numpy as np
import pylorentz
from typing import Tuple
from dataclasses import dataclass


@dataclass
class Particle():
    """
    Initialise particle from provided data, most of which is optional.
        pdg: id of particle according to pdg database convention
        status: status code of particle following the Pythia convention
        mothers: tuple containing index of mother particles if applicable
        daughters: tuple containing index of daughter particles if applicable
        cols: tuple containing col,anticol values for partons if provided
        px, py, pz, e: floats, momentum components for particles
        m: float, mass of the particle, not as calculated from its momentum
        check_on_shell: bool, whether to check if provided particle is on-shell
    """

    # Review value of tolerance
    TOL = 1E-1

    pdg: int = 0
    status: int = 0
    mothers: Tuple[int, int] = (0, 0)
    daughters: Tuple[int, int] = (0, 0)
    cols: Tuple[int, int] = (0, 0)
    px: float = 0.
    py: float = 0.
    pz: float = 0.
    e: float = 0.
    m: float = 0.
    check_on_shell: bool = True

    def __post_init__(self):
        """
        Check on shell within tolerance TOL
        """
        self.momentum = pylorentz.Momentum4(self.e, self.px, self.py, self.pz)
        if (self.check_on_shell):
            self.check_on_shell_particles()

    def momentum(self):
        """
        Returns the momentum of the particle.
        """
        return self.momentum

    def m_calc(self):
        """
        Calculate mass from momentum.
        """
        p = self.momentum
        return np.sqrt(np.abs(p.e**2 - p.p_x**2 - p.p_y**2 - p.p_z**2))

    def rap(self):
        """
        Wrapper around rapidity from pylorentz.
        """
        p = self.momentum
        if (p.e - p.p_z == 0.):
            return np.inf
        elif (p.e + p.p_z == 0.):
            return -np.inf

        return 0.5 * np.log((p.e + p.p_z)/(p.e - p.p_z))

    def phi(self):
        """
        Wrapper around phi from pylorentz.
        """
        p = self.momentum
        return np.arctan2(p.p_y, p.p_x)

    def perp(self):
        """
        Wrapper around p_T from pylorentz.
        """
        p = self.momentum
        return np.sqrt(p.p_x**2 + p.p_y**2)

    def p_x(self):
        """
        Wrapper around p_x
        """
        return self.momentum.p_x

    def p_y(self):
        """
        Wrapper around p_x
        """
        return self.momentum.p_y

    def p_z(self):
        """
        Wrapper around p_x
        """
        return self.momentum.p_z

    def E(self):
        """
        Wrapper around p_x
        """
        return self.momentum.e

    def is_parton(self):
        """
        Compares the pdg id code from init to a container of parton pdg codes.
        """
        return (abs(self.pdg) in [1, 2, 3, 4, 5, 6, 21])

    def is_final(self):
        """
        Returns true if the (Pythia) status code of the particle is positive.
        """
        return (self.status > 0)

    def is_incoming(self):
        """
        Returns true if the (Pythia) status code of the particle is negative.
        """
        return (self.status < 0)

    def check_on_shell_particles(self):
        """
        Checks on-shellness of the particle compared to the init mass to
        within a tolerance set to 1E-3 by default.
        """
        calc = self.m_calc()

        if (self.m < 0.):
            raise(ValueError("Particle has negative mass as input"))

        elif (self.m == 0.):
            if (np.abs(calc) > Particle.TOL):
                raise(ValueError("Particle is not on shell"))
            else:
                return

        elif (np.abs((calc - self.m) / self.m) > Particle.TOL):
            raise(ValueError("Particle is not on shell"))
