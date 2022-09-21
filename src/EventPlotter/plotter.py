import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np
from particle import Particle

np.random.seed(10)

cividis = cm.get_cmap('YlOrRd', 256)
newcolors = cividis(np.linspace(0, 1, 256))
white = np.array([256/256, 256/256, 256/256, 1])
newcolors[:1, :] = white
newcmp = ListedColormap(newcolors)


def read_pythia(listing, verbose: bool=False):
    particles = []
    for x in listing:
        if (len(x)>2 and x[-2] != "-"):
            info = x.split()
            if (info[0] != "no" and info[0] != "Charge"):
                particles.append(Particle(int(info[1]), int(info[3]), (int(info[4]), int(info[5])),
                                  (int(info[6]), int(info[7])), (int(info[8]), int(info[9])),
                                  float(info[10]), float(info[11]), float(info[12]), float(info[13]),
                                  float(info[14]), check_on_shell=False))

    if (verbose):
        for idx, p in enumerate(particles):
            print(idx, p.pdg, p.status, p.mothers, p.daughters, p.cols, p.momentum, p.m)
    return particles


def parse(file_in: str, verbose: bool=False):
    with open(file_in) as fstream:
        data = fstream.read()
        events = [[a for a in x.split("\n")] for x in data.split("\n\n\n\n\n")]
        zed = [read_pythia(event) for event in events]
        return zed


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
 
   # for idx, point in enumerate(y_phi):
   #     #angle = np.random.uniform(-3.14, 3.14)
   #     #plt.annotate(str(round(point[3], 2)), xy=(point[1]+0.25*np.cos(4.*idx*np.pi/len(y_phi)), point[2]+0.25*np.sin(4.*idx*np.pi/len(y_phi))), color="white", fontsize=4)
   #     #plt.annotate("$y=$%.2f" % round(point[1], 2), xy=(point[1]+0.1*point[2], point[2]), color="white", fontsize=4)
   #     if (point[3] > 40):
   #         plt.annotate("%.2f" % round(point[3], 2), xy=(point[1]+0.1*point[2], point[2]), color="white", fontsize=4)
   # ax = plt.axes()
   # ax.add_patch(plt.Circle((-0.28706, 0.514745), 0.4, fill=False, color="red"))
   # ax.add_patch(plt.Circle((1.29097, -2.62615), 0.4, fill=False, color="red"))

   #plt.axvline(x=-4.4, color="black", linestyle="--")
   #plt.axvline(x=4.4, color="black", linestyle="--")
    bar.set_label(r'$p_\perp \quad [\textrm{GeV}]$')
    plt.savefig(title, bbox_inches='tight')
    plt.clf()
    return image


input_events = parse("input_event")
img = np.zeros((50, 50))
prods = np.zeros((2,4))
for ev in input_events:
    l = get_image(ev)
    img += l[0]
    prods += np.array(l[1])

img /= len(input_events)
prods /= len(input_events)

plot_y_phi(img, prods, "input_wm_5j.pdf")
