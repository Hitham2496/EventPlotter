#!/usr/bin/env python
"""
Event file reader class definition
"""
from .event import Event
from .particle import Particle
import xml.etree.ElementTree as ET


class Reader():

    def __init__(self, filename: str):
        """
        Initialises an event reader object from the event file `filename`.
        """

    def read_next(self, verbose: bool = False):
        """
        Advances the reader by one event.
        """

    def __exit__(self):
        """
        Closes the event file buffer on destruction if needed.
        """


class ReaderLHEF(Reader):

    def __init__(self, filename: str):
        """
        Initialises a LHE reader object from the event file `filename` ending in .lhe,
        we use the xml implementation of the LHE format to simplify te implementation.
        """
        if not str(filename).endswith(".lhe"):
            raise(ValueError("Event file must end with the .lhe extension."))

        self.buffer = ET.iterparse(filename, events = ("start", "end") )
        self.current_event = None

    def read_next(self, verbose: bool = False):
        """
        Advances the reader by one event.
        """
        xml_event = next(self.buffer)

        while xml_event[1].tag != "event":
            xml_event = next(self.buffer)

        while not (xml_event[1].tag == "event" and xml_event[0] == "end"):
            xml_event = next(self.buffer)

        text_event = xml_event[1].text.strip().split("\n")
        print(text_event)




class ReaderPythia(Reader):

    def read_next(self, verbose: bool = False):
        return 0
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
