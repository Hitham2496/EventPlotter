#!/usr/bin/env python
"""
Event class definition
"""
import numpy as np
import pylorentz
from dataclasses import dataclass, field


@dataclass
class Event():
    """
    Saves information of particles in an event and sets
    additional information of event by default. Arguments:
        particles: array-like container of EventPlotter Particles
        root_s: float, sqrt CoM energy of interaction
        mur: float, renormalisation scale
        muf: float, factorisation scale
        set_info: bool, sets the x+/- values of the incoming particles and
                  the CoM energy of the hard interaction
        x_plus: float, x value of +z incoming particle
        x_minus: float, x value of -z incoming particle
        wgt: float, event weight
    """

    particles: list = field(default_factory=list)
    root_s: float = 0.
    mur: float = 0.
    muf: float = 0.
    set_info: bool = True
    x_plus: float = 0.
    x_minus: float = 0.
    wgt: float = 1.


    def __post_init__(self):
        """
        Find incoming particles and set info if not provided in constructor.
        """
        self.find_incoming()
        if (not self.check_momentum()):
            raise(ValueError("""Momentum not conserved in event"""))

        if (self.set_info):
            self.setup()
            return

    def __str__(self):
        rep = "-"*10+"EventPlotter event listing"+"-"*10
        rep += "\nno.\tid\tstatus\tmomentum (px, py, pz, e)"
        for idx, p in enumerate(self.particles):
            rep += "\n"
            rep += "{:<4}\t{:<4}\t{:<2}\t({:<12}\t".format(idx, p.pdg, p.status, p.p_x())
            rep += "{:<12}\t{:<12}\t{:<12})".format(p.p_y(), p.p_z(), p.E())
        return rep

    def find_incoming(self):
        """
        Finds the positions of the incoming particles in the particles
        container.
        """
        incoming = [-1, -1]
        beams = [-1, -1]
        for idx, part in enumerate(self.particles):
            if (part.is_incoming() and part.E() == self.root_s / 2.):
                if (part.p_z() > 0.):
                    beams[0] = idx
                if (part.p_z() < 0.):
                    beams[1] = idx
            elif ((part.is_incoming()) and (part.perp() == 0.)
                  and (part.p_z() != 0.) and (part.E() != 0.)):
                side = int(part.p_z() / np.abs(part.p_z()))
                if (side == 1):
                    incoming[0] = idx
                elif (side == -1):
                    incoming[1] = idx
            elif (part.is_incoming()):
                raise(ValueError("Incoming particle has non-zero transverse momentum"))
            if (incoming[0] != -1 and incoming[1] != -1):
                self.beams = beams
                self.incoming = incoming
                return

        if (incoming[0] == -1 or incoming[1] == -1):
            raise(ValueError("One or more incoming particles was not found"))

    def setup(self):
        """
        Calculates global quantities of event including:
        centre of mass energy, pdf energy fractions. This
        method should be called if any modification to the
        particle content has been applied after init.
        """
        self.root_s_hat = self.calc_root_s_hat()
        self.x_plus = self.calc_x(1)
        self.x_minus = self.calc_x(-1)

    def calc_root_s_hat(self):
        """
        Calculates the hard interaction CoM energy of an event.
        """
        inc = self.incoming
        p_ini = pylorentz.Momentum4(0., 0., 0., 0.)
        p_ini += self.particles[inc[0]].momentum
        p_ini += self.particles[inc[1]].momentum
        if (p_ini.p_z == 0. or p_ini.e == 0. or p_ini.p_t != 0):
            raise(ValueError("""Event does not contain incoming particles
                             of valid momentum."""))

        return p_ini.m

    def calc_x(self, direction: int):
        """
        Calculates the x value for each particle incoming along the beam axis,
        admits the direction (+1 for positive z, -1 for negative z) as a
        parameter. Assumes equal energy beams.
        """
        inc = self.incoming
        if (direction == 1):
            return self.particles[inc[0]].E() / (self.root_s / 2.)
        elif (direction == -1):
            return self.particles[inc[1]].E() / (self.root_s / 2.)
        else:
            raise(ValueError("""The direction must be +/-1 for the incoming
                             particles for the +/- z axis respectively."""))

    def check_momentum(self, tol: float = 1E-2):
        """
        Checks momentum conservation in the event to within a tolerance set to
        1E-2 by default.
        """
        inc = self.incoming
        EPS = 1E-2
        p_check = pylorentz.Momentum4(0., 0., 0., 0.)
        p_check += self.particles[inc[0]].momentum
        p_check += self.particles[inc[1]].momentum
        for idx, part in enumerate(self.particles):
            if (part.is_final()):
                p_check -= part.momentum

        for comp in p_check:
            if (abs(comp) > EPS):
                return False

        return True
