#!/usr/bin/env python
"""
Event file reader class definition.
"""
from .event import Event
from .particle import Particle
import xml.etree.ElementTree as ET


class Reader():
    """
    Bare reader class to allow custom derived classes for new formats.
    """

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
        Initialises a LHE reader object from the event file `filename` ending in .lhe.

        We use the xml implementation of the LHE format to simplify the implementation.
        :param filename: str name of event file.
        :param wgt_idx: optional int indexing which weight to save.
        """
        if not str(filename).endswith(".lhe"):
            raise(ValueError("Event file must end with the .lhe extension."))

        self.buffer = ET.iterparse(filename, events=("start", "end"))
        self.current_event = None
        self.init_info = None
        self.wgt_idx = wgt_idx
        self.beams = []
        self.com_energy = 0.
        while not self.init_info:
            tmp_xml_event = next(self.buffer)
            if tmp_xml_event[1].tag == "init":
                self.set_init_info(tmp_xml_event[1].text)


    def advance(self):
        """
        Wrapper around next for event buffer
        """
        return next(self.buffer)

    def __iter__(self):
        """
        Use instance of the class as a wrapper for interaction with the buffer
        """
        return self

    def __next__(self):
        """
        Advances the reader by one event.
        """
        xml_event = self.advance()
        wgts = None

        # Write initialisation information if provided in LHE file
        while xml_event[1].tag != "event":
            if xml_event[0] == "end" and xml_event[1].tag == "init":
                self.set_init_info(xml_event[1].text)

            xml_event = self.advance()

        # Look only at events for event record
        while not (xml_event[1].tag == "event" and xml_event[0] == "end"):
            # Keep weights if provided
            if xml_event[1].tag == "weights" and xml_event[0] == "end":
                wgts = [float(x) for x in xml_event[1].text.strip().split()]

            xml_event = self.advance()

        text_event = xml_event[1].text.strip().split("\n")

        # Add particles to event container, starting with system and beams
        parts = []
        parts.append(Particle())
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
        Set info from initialisation of LHE file.

        :param info: str, the xml data in string format.
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
