"""
EventPlotter: Comprehensive plotting and analysis of
events in high energy physics.

This package includes classes for particles and events
in high energy physics (HEP) as well as functionality
for reading events as output in the LHE format used for
MC event generators.

The plotter class allows for a novel method of analysis
for events, including invaluable visualisation in the
rapidity-azimuthal angle plane.
"""
from .particle import Particle
from .event import Event
from .reader import Reader, ReaderLHEF
from .plotter import Plotter
from .utils import *
