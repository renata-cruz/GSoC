import numpy as np
from scipy.spatial.distance import cdist
import numba
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Circles:
    def __init__(self, distribution, voxel_size, max_iterations=1e2, **kwargs):
        """Class to create packed circles with radii sampled from a given ditribution."""

        self.voxel_size = voxel_size
        self.max_iterations = max_iterations

        if distribution == "uniform":
            self.low = kwargs["low"]
            self.high = kwargs["high"]
            self.size = kwargs["size"]
            self.sampled_radii = np.random.unforml(self.low, self.high, self.size)

        elif distribution == "normal":
            self.loc = kwargs["loc"]
            self.scale = kwargs["scale"]
            self.size = kwargs["size"]
            self.sampled_radii = np.random.normal(self.loc, self.scale, self.size)

        elif distribution == "gamma":
            self.shape = kwargs["shape"]
            self.scale = kwargs["scale"]
            self.size = kwargs["size"]
            self.sampled_radii = np.random.gamma(self.shape, self.scale, self.size)

        else:
            print("distribution not found")

        self.sampled_radii = np.sort(self.sampled_radii)[::-1]

    def _mirrored_circles(self, C, r):
        """Create mirrored versions of a circle in the eight surrounding voxels.
        This will add a periodic boundary condition to the central voxel.

        Parameters
        ----------
        C : tuple
            Center of circle C(x, y).
        r : float
            Radius of the circle.

        Returns
        -------
        mirrors : numpy.ndarray
            Array with center coordinates for the mirrors and their radii.
        """
        x, y = C
        mirrors = np.array(
            [
                [x, y, r],
                [x - self.voxel_size, y, r],
                [x + self.voxel_size, y, r],
                [x, y - self.voxel_size, r],
                [x, y + self.voxel_size, r],
                [x - self.voxel_size, y - self.voxel_size, r],
                [x + self.voxel_size, y - self.voxel_size, r],
                [x - self.voxel_size, y + self.voxel_size, r],
                [x + self.voxel_size, y + self.voxel_size, r],
            ]
        )
        return mirrors

    @numba.jit
    def _overlapping_mirrors(self, mirrors, placed_mirrors):
        """Check if any circle in a mirror position overlaps with other circles.

        Parameters
        ----------
        mirrors : numpy.ndarray
            Array with center coordinates for the mirrors positions of a circle and their radii.
        placed_mirrors : numpy.ndarray
            Stored center coordinates for the mirrors positions of a circle and their radii.

        Returns
        -------
        boolean
        """
        x = mirrors[:, :2]
        y = placed_mirrors[:, :2]
        d = cdist(x, y)
        r_m = np.unique(mirrors[:, 2])
        r_pm = placed_mirrors[:, 2]
        overlap = 0
        for col, r in zip(range(len(placed_mirrors)), r_pm):
            if np.any(d[:, col] < (r + r_m)):
                overlap += 1
        if overlap == 0:
            return False
        return True

    def _boundaries(self):
        """Define the 2D boundaries of the voxel.

        Returns
        -------
        boundaries : numpy.ndarray
            Array with 2D boundaries of the voxel.
        """
        top = [(0, self.voxel_size), (self.voxel_size, self.voxel_size)]
        bottom = [(0, 0), (self.voxel_size, 0)]
        left = [(0, 0), (0, self.voxel_size)]
        right = [(self.voxel_size, 0), (self.voxel_size, self.voxel_size)]
        boundaries = [bottom, left, top, right]
        return np.asarray(boundaries)

    def _dist_lineseg_point(x, y, p1, p2):
        """Distance between a point C(x,y) and a boundary AB.

        Parameters
        ----------
        C : tuple
            Center of circle C(x, y).
        a : numpy.ndarray
            Array with the catesian coordinates of point A.
        b : numpy.ndarray
            Array with the catesian coordinates of point B.

        Returns
        -------
        distance : numpy.ndarray
            Distance between point C and the boundary AB.
        """
        C = (x, y)
        C = np.atleast_2d(C)
        d = np.divide(p2 - p1, np.linalg.norm(p2 - p1))
        s = np.dot(p1 - C, d)
        t = np.dot(C - p2, d)
        h = np.maximum.reduce([s, t, np.zeros(len(C))])
        c = np.cross(C - p1, d)
        distance = np.hypot(h, c)
        return distance

    def _periodic_circles(self, mirrors):
        """Selection of circles contained inside the voxel and interating with the boundaries.

        Parameters
        ----------
        mirrors : numpy.ndarray
            Array with the catesian coordinates of point P.

        Returns
        -------
        periodic_circles : numpy.ndarray
            Array with the periodically bounded circles.
        """
        boundaries = self._boundaries()
        periodic_circles = []
        for mirror in mirrors:
            x, y, r = mirror
            if 0 <= x <= self.voxel_size and 0 <= y <= self.voxel_size:
                periodic_circles.append(mirror)
            for b in boundaries:
                p1, p2 = b
                p1 = np.asarray(p1)
                p2 = np.asarray(p2)
                d = self._dist_lineseg_point(x, y, p1, p2)
                if d < r:
                    periodic_circles.append(mirror)
        periodic_circles = np.unique(periodic_circles, axis=0)
        return np.asarray(periodic_circles)

    def place_circles(self):
        """Pack circles in a voxel with periodic boundaries.

        Returns
        -------
        circles : numpy.ndarray
            Array with the center coordinates and radii of the cirlces placed in the voxel.
        """
        placed_mirrors = np.zeros((len(self.sampled_radii) * 9, 3))
        filled_positions = 1
        for r in self.sampled_radii:
            placed = False
            i = 0
            while not placed and i < self.max_iterations:
                i += 1
                x, y = np.random.random(2) * self.voxel_size
                mirrors = self._mirrored_circles((x, y), r)
                if np.all(placed_mirrors == 0):
                    for mirror, k in zip(mirrors, range(len(mirrors))):
                        placed_mirrors[k] = mirror
                    placed = True
                else:
                    intersects = False
                    if self._overlapping_mirrors(mirrors, placed_mirrors):
                        intersects = True
                        break
                    if not intersects:
                        interval = filled_positions * 9
                        for mirror, k in zip(
                            mirrors, range(interval, len(mirrors) + interval)
                        ):
                            placed_mirrors[k] = mirror
                        placed = True
                        filled_positions += 1
        circles = self._periodic_circles(placed_mirrors)
        return circles


circles = Circles(
    distribution="gamma", voxel_size=1e-4, shape=3, scale=1e-6, size=int(5e2)
).place_circles()

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot()
for circle in circles:
    circle = plt.Circle((circle[0], circle[1]), circle[2], fill=False)
    ax.add_artist(circle)
ax.set_xlim([-1e-4, 2e-4])
ax.set_ylim([-1e-4, 2e-4])
plt.axvline(x=0, color="r")
plt.axvline(x=1e-4, color="r")
plt.axhline(y=0, color="r")
plt.axhline(y=1e-4, color="r")
plt.show()
