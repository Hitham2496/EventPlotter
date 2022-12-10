#!/usr/bin/env python
"""
Plotter class definition.
"""
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
import numpy as np
from typing import Tuple
from .event import Event
from .utils import is_number


class Plotter():

    def __init__(
                 self,
                 rap_extent: Tuple[float, float] = (-7, 7),
                 phi_extent: Tuple[float, float] = (-3.14, 3.14),
                 bins: int = 50,
                 chosen_map: str = r"YlOrRd",
                 min_val: int = 1,
                 custom_z_axis = None,
                 z_label: str = r"$p_\perp \quad [\textrm{GeV}]$",
                 include_wgt: bool = False
                ):
        """
        Initialise Plotter class, arguments:
            rap_extent: tuple for the limits along the rapidity axis.
            phi_extent: tuple for the limits along the phi axis (-pi, pi).
            bins: number of bins along each axis.
            chosen_map: string denoting the matplotlib colour map to be used.
            min_val: minimum value between 0 and 256 for colour map, beneath which
                     the colour will be set as white.
            custom_z_axis: optional, Callable function of Particle objetc to use as
                           the z-axis of the 3d plot, by default the pT of the
                           particle is used.
            z_label: custom label for the z-axis
            include_weight: whether to multiply the z-axis value by the event
                            weight
        """
        # check rapidity extent is valid
        if (isinstance(rap_extent, list) or isinstance(rap_extent, Tuple)):
            if (len(rap_extent) != 2):
                raise(TypeError("Rapidity extent must have two components only"))
            else:
                for bound in rap_extent:
                    if (not is_number(bound)):
                        raise(TypeError("Rapidity bounds must be float or int"))
            self.rap_extent = sorted(rap_extent)
        else:
            raise(TypeError("Rapidity extent must be 2 component array-like"))

        # check phi extent is valid
        if (isinstance(phi_extent, list) or isinstance(phi_extent, Tuple)):
            if (len(phi_extent) != 2):
                raise(TypeError("Phi extent must have two components only"))
            else:
                for bound in phi_extent:
                    if (not is_number(bound)):
                        raise(TypeError("Phi bounds must be float or int"))
                    elif (np.abs(bound) >= np.pi):
                        raise(ValueError("Phi bound must be in (-pi, pi)"))

            self.phi_extent = sorted(phi_extent)
        else:
            raise(TypeError("Phi extent must be 2 component array-like"))

        # check bins is int-like >= 1
        if (not is_number(bins)):
            raise(TypeError("Number of bins must be int"))
        elif (bins < 1):
            raise(ValueError("Number of bins must be larger than 0"))

        # check z_label is str
        if (not isinstance(z_label, str)):
            raise(TypeError("z label must be a string"))

        # check chosen_map is str
        if (not isinstance(chosen_map, str)):
            raise(TypeError("chosen color map must be a string"))

        # check include_wgt is bool
        if (not isinstance(include_wgt, bool)):
            raise(TypeError("include_wgt must be a bool"))

        self.bins = int(bins)
        self.z_func = custom_z_axis
        self.z_label = z_label
        self.include_wgt = include_wgt
        self.get_colormap(chosen_map, min_val)

    def get_colormap(self, chosen_map: str = "YlOrRd", min_val: int = 1):
        """
        Sets a chosen color map for the z-axis with all values beneath
        min_val/256 as white. Can be called again with new arguments
        after initialisation for alteration.
        """
        if (min_val < 0 or min_val > 256):
            raise(ValueError("Minimum value in colormap must be between 0 and 256"))

        set_map = cm.get_cmap(chosen_map, 256)
        new_colors = set_map(np.linspace(0, 1, 256))
        white = np.array([256/256, 256/256, 256/256, 1])
        new_colors[:int(min_val), :] = white
        self.color_map = ListedColormap(new_colors)

    def get_image(self, event: Event = None, idx_products = None):
        """
        Returns a square numpy array of dimension bins*bins, populated with the
        z-axis values corresponding to each point in rapidity-azimuthal angle
        space. Option to provide an array or array-like container of indices for
        decay products (or other particles not to be included in the heatmap)
        as 'idx_products'.
        """
        y_phi = []
        if (not idx_products):
            for idx, p in enumerate(event.particles):
                if (p.is_final() and p.is_parton()):
                    fill_val = self.z_func(p) if (self.z_func) else p.perp()
                    if (not is_number(fill_val)):
                        raise(TypeError("custom z function must return a float or int"))
                    fill_val *= event.wgt if (self.include_wgt) else 1
                    y_phi.append([idx, p.rap(), p.phi(), fill_val])
        else:
            for idx, p in enumerate(event.particles):
                if (p.is_final() and p.is_parton() and (idx not in idx_products)):
                    fill_val = self.z_func(p) if (self.z_func) else p.perp()
                    if (not is_number(fill_val)):
                        raise(TypeError("custom z function must return a float or int"))
                    fill_val *= event.wgt if (self.include_wgt) else 1
                    y_phi.append([idx, p.rap(), p.phi(), fill_val])

        y_phi.sort(key = lambda x: x[3])

        image = np.zeros((self.bins, self.bins))

        for j, part in enumerate(y_phi):
            phi = np.abs(np.linspace(self.phi_extent[0], self.phi_extent[1],
                         self.bins) - part[2]).argmin()
            rap = np.abs(np.linspace(self.rap_extent[0], self.rap_extent[1],
                         self.bins) - part[1]).argmin()
            if ((part[1] > self.rap_extent[0] and part[1] < self.rap_extent[1])
                and (part[2] > self.phi_extent[0] and part[2] < self.phi_extent[1])):  # noqa: E129
                image[phi, rap] += part[3]

        if (idx_products):
            y_phi_products = []
            for loc in idx_products:
                p = event.particles[loc]
                fill_val = self.z_func(p) if (self.z_func) else p.perp()
                if (not is_number(fill_val)):
                    raise(TypeError("custom z function must return a float or int"))
                fill_val *= event.wgt if (self.include_wgt) else 1
                y_phi_products.append([p.pdg, p.rap(), p.phi(), fill_val])

            y_phi_products.sort(key = lambda x: x[3])
            return image, y_phi_products

        return image

    def plot_y_phi(self, image = None, products = None, title: str = "event.pdf"):
        """
        Renders a square heatmap of the y-phi plane given:
            image: a (bins x bins) dimensional numpy array
            products: (optional) array-like container [id,y,phi,fill_value]
                      for particles to be displayed as scatter points
            title: title of the figure to be saved, by default 'event.pdf'
        """
        if (image is None):
            raise(ValueError("Must provide an image to plot"))
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plt.xlabel(r'$y$')
        plt.ylabel(r'$\phi \quad [\textrm{rad}]$')

        rap_length = np.abs(self.rap_extent[0] - self.rap_extent[1])
        phi_length = np.abs(self.phi_extent[0] - self.phi_extent[1])
        plt.imshow(image, interpolation='none', origin='lower', aspect=rap_length/phi_length,
                   extent=[self.rap_extent[0], self.rap_extent[1], self.phi_extent[0],
                           self.phi_extent[1]], cmap=self.color_map)

        bar = plt.colorbar()
        if (products):
            for pt in products:
                plt.scatter(pt[1], pt[2], c="black", marker="x")
                plt.annotate(r"id="+str(round(np.abs(pt[0]))), (pt[1]+0.1, pt[2]+0.1))
        # bar.ax.yaxis.set_ticks([point[3] for point in y_phi], minor=True)

        bar.set_label(self.z_label)
        plt.savefig(title, bbox_inches='tight')
        plt.clf()
        return image
