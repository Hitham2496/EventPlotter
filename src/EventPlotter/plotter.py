import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np
from typing import Tuple
from particle import Particle


class Plotter():


    def __init__(
                 self,
                 rap_extent: Tuple[float, float] = (-7,7),
                 phi_extent: Tuple[float, float] = (-3.14,3.14),
                 bins: int = 50,
                 chosen_map: str = "YlOrRd",
                 min_val: int = 1,
                 custom_z_axis = None,
                 z_label: str = r"$p_\perp$"
                 include_wgt: bool = False
                ):
        """
        Initialise plotter class, arguments:
            rap_extent: tuple for the limits along the rapidity axis.
            phi_extent: tuple for the limits along the phi axis.
            bins: number of bins along each axis.
            chosen_map: string denoting the matplotlib colour map to be used.
            min_val: minimum value between 0 and 256 for colour map, beneath which
                     the colour will be set as white.
            custom_z_axis: optional, Callable function of four momenta to use as
                           the z-axis of the 3d plot, by default the pT of the
                           particle is used.
            z_label: custom label for the z-axis, by default set to $p_\perp$
            include_weight: whether to multiply the z-axis value by the event
                            weight
        """
        self.rap_extent = sorted(rap_extent)
        self.phi_extent = sorted(phi_extent)
        self.bins = int(bins)
        self.z_function = custom_z_axis
        self.z_label = z_label
        self.include_wgt = include_wgt
        self.get_colormap(chosen_map, min_val)


    def get_colormap(self, chosen_map: str="YlOrRd", min_val: int=1):
        """
        Sets a chosen color map for the z-axis with all values beneath
        min_val/256 as white.
        """
        if (min_val < 0 or min_val > 256):
            raise(ValueError("Minimum value in colormap must be between 0 and 256"))

        set_map = cm.get_cmap(chosen_map, 256)
        new_colors = set_map(np.linspace(0, 1, 256))
        white = np.array([256/256, 256/256, 256/256, 1])
        new_colors[:int(min_val), :] = white
        self.color_map = ListedColormap(newcolors)


    def get_image(self, event: Event = None):
        """
        Returns a square numpy array of dimension bins*bins, populated with the
        z-axis values corresponding to each point in rapidity-azimuthal angle
        space.
        """
        y_phi = []
        y_phi_products = []
        for idx, p in enumerate(event.particles):
            if (p.is_final() and p.is_parton()):
                y_phi.append([idx, p.rap(), p.phi(), p.perp()])
            elif (p.is_final() and (not p.is_parton()) and (not np.abs(p.status) > 62)):
                y_phi_products.append([p.pdg, p.rap(), p.phi(), p.perp()])

        y_phi.sort(key = lambda x: x[3])
        y_phi_products.sort(key = lambda x: x[3])

        image = np.zeros((self.bins, self.bins))

        for j, part in enumerate(y_phi):
            y = np.abs(np.linspace(self.phi_extent[0], self.phi_extent[1],
                       self.bins) - part[2]).argmin()
            x = np.abs(np.linspace(self.rap_extent[0], self.rap_extent[1],
                       self.bins) - part[1]).argmin()
            if ((part[1] > self.rap_extent[0] and part[1] < self.rap_extent[1])
                and (part[2] > self.phi_extent[0] and part[2] < self.phi_extent[1])):
                image[y,x] += part[3]

        return [image, y_phi_products]


    def plot_y_phi(self, image: np.array, products = 0, title="event.pdf"):
        """
        Renders a 3D lego plot of the y-phi plane
        """

        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plt.xlabel(r'$y$')
        plt.ylabel(r'$\phi \quad [\textrm{rad}]$')

        plt.imshow(image, interpolation='none', origin='lower', aspect=4.4/3.14, extent=[-4.4, 4.4, -3.14, 3.14],
                   cmap=newcmp)

        bar = plt.colorbar()
        if ( not (isinstance(products,int)) ):
            for pt in products:
                plt.scatter([pt[1]], [pt[2]], marker='x', color='black')
                if (round(abs(pt[0])) == 11):
                    plt.annotate(r"$e^-$", (pt[1]+0.1, pt[2]+0.1))
                elif (round(abs(pt[0])) == 12):
                    plt.annotate(r"$\overline{\nu}$", (pt[1]+0.1, pt[2]+0.1))
        # bar.ax.yaxis.set_ticks([point[3] for point in y_phi], minor=True)

        bar.set_label(r'$p_\perp \quad [\textrm{GeV}]$')
        plt.savefig(title, bbox_inches='tight')
        plt.clf()
        return image
