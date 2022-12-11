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

    def read_next(self):
        """
        Advances the reader by one event.
        """

    def __exit__(self):
        """
        Closes the event file buffer on destruction if needed.
        """


class ReaderLHEF(Reader):

    def __init__(self, filename: str, wgt_idx: int=None):
        """
        Initialises a LHE reader object from the event file `filename` ending in .lhe,
        we use the xml implementation of the LHE format to simplify te implementation.
        Optionally add a weight index to initialise the events with weights as provided
        in the file.
        """
        if not str(filename).endswith(".lhe"):
            raise(ValueError("Event file must end with the .lhe extension."))

        self.buffer = ET.iterparse(filename, events=("start", "end"))
        self.current_event = None
        self.init_info = None
        self.wgt_idx = wgt_idx
        self.beams = []
        self.com_energy = 0.

    def read_next(self):
        """
        Advances the reader by one event.
        """
        xml_event = next(self.buffer)
        wgts = None

        # Write initialisation information if provided in LHE file
        while xml_event[1].tag != "event":
            if xml_event[0] == "end" and xml_event[1].tag == "init":
                self.set_init_info(xml_event[1].text)

            xml_event = next(self.buffer)

        # Look only at events for event record
        while not (xml_event[1].tag == "event" and xml_event[0] == "end"):
            # Keep weights if provided
            if xml_event[1].tag == "weights" and xml_event[0] == "end":
                wgts = [float(x) for x in xml_event[1].text.strip().split()]

            xml_event = next(self.buffer)

        text_event = xml_event[1].text.strip().split("\n")

        # Add particles to event container, starting with system and beams
        parts = []
        parts.append(Particle(status=-1))
        parts.append(self.beams[0])
        parts.append(self.beams[1])
        for idx, line in enumerate(text_event[1:]):
            data = line.split()
            parts.append(Particle(pdg=int(data[0]),
                                  status=int(data[1]),
                                  cols=(int(data[4]), int(data[5])),
                                  px=float(data[6]),
                                  py=float(data[7]),
                                  pz=float(data[8]),
                                  e=float(data[9]),
                                  m=float(data[10]),
                                  check_on_shell=False
                                  )
                         )

        if self.wgt_idx is not None:
            return Event(particles=parts,
                         root_s=self.com_energy,
                         set_info=False,
                         wgt=wgts[self.wgt_idx]
                         )

        return Event(particles=parts, root_s=self.com_energy, set_info=False)

    def set_init_info(self, info: str=None):
        """
        Set info from initialisation of LHE file incl. beams given
        the xml data in string format.
        """
        if self.init_info is None:
            init_info = [float(i) for i in info.strip().split("\n")[0].split()]
            self.beams.append(Particle(pdg=int(init_info[0]),
                                       status=-1,
                                       pz=init_info[2],
                                       e=init_info[2])
                              )
            self.beams.append(Particle(pdg=int(init_info[1]),
                                       status=-1,
                                       pz=-init_info[3],
                                       e=init_info[3])
                              )
            self.com_energy = self.beams[0].E() + self.beams[1].E()
            self.init_info = init_info


class ReaderPythia(Reader):

    def read_next(self):
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
