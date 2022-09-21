import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np
from particle import Particle


class Plotter():

    def get_colormap(self, chosen_map: str='YlOrRd', min_val: int=1):

        if (min_val < 1 or min_val > 256):
            raise(ValueError("Minimum value in colormap must be between 1 and 256"))

        set_map = cm.get_cmap(chosen_map, 256)
        new_colors = set_map(np.linspace(0, 1, 256))
        white = np.array([256/256, 256/256, 256/256, 1])
        new_colors[:int(min_val), :] = white
        self.color_map = ListedColormap(newcolors)

    def get_image(particles, bins=(50, 50)):
        y_phi = []
        y_phi_products = []
        for idx, p in enumerate(particles):
            if (p.is_final() and p.is_parton()):
                y_phi.append([idx, p.rap(), p.phi(), p.perp()])
            elif (p.is_final() and (not p.is_parton()) and (not np.abs(p.status) > 62)):
                y_phi_products.append([p.pdg, p.rap(), p.phi(), p.perp()])

        y_phi.sort(key=lambda x: x[3])
        y_phi_products.sort(key=lambda x: x[3])

        image = np.zeros((bins[0],bins[1]))

        for j, part in enumerate(y_phi):
            y = np.abs(np.linspace(-3.14, 3.14, bins[1]) - part[2]).argmin()
            x = np.abs(np.linspace(-7., 7., bins[0]) - part[1]).argmin()
            if (np.abs(part[1]) < 7. and np.abs(part[2]) < 3.14):
                image[y,x] += part[3]

        return [image, y_phi_products]


    def plot_y_phi(image, products = 0, title="event.pdf"):
        """Makes lego plot of the y-phi plane"""

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
