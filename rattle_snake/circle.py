"""
draw the concentric circles
"""
import matplotlib.pyplot as plt
import numpy as np


class RealmMap:
    """Class for holding the map of the realms"""

    map_file_name = "images/weird_science_realm.png"
    colors = ["b", "g", "r", "cyan"]
    markers = ["*", ".", "p", "s", "v"]

    def __init__(self, title: str, num_circles: int = 4):
        self.title = title
        self.num_circles = num_circles
        self.stratum_radii = 2.0
        self.stratum_boundaries = [
            ((i) * self.stratum_radii, (i + 1) * self.stratum_radii)
            for i in range(num_circles)
        ]
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect(1)
        plt.title("The world of beings -- weird science")
        self.draw_circles()

    def save(self):
        """Save the image"""
        plt.savefig(self.map_file_name)

    def generate_points(self, k: int = 3, min_support: int = 3, max_support: int = 10):
        """Generate and draw points.

        There are k population centers in each stratum.
        For each population center we generate a random nubmer of
        supporting/surround nodes.
        """
        stratum_num = 0
        for color_num, bounds in enumerate(self.stratum_boundaries):
            print(f"stratum number {stratum_num}")
            stratum_num += 1

            # generate the pop centers
            for i in range(k):
                length = np.random.uniform(bounds[0], bounds[1])
                print(f"length: {length}")
                angle = np.pi * np.random.uniform(0, 2)

                x = length * np.cos(angle)
                y = length * np.sin(angle)
                print(self.stratum_boundaries[i][0], self.stratum_boundaries[i][1])
                print(i, ":", x, y)

                self.ax.scatter(
                    x,
                    y,
                    color=self.colors[color_num],
                    marker=self.markers[i],
                    linewidths=3.0,
                )

                # generate supporting nodes
                num_support = np.random.randint(min_support, max_support + 1)
                for _ in range(num_support):
                    # controls how close the points are
                    delta = 0.2
                    l = np.random.uniform(length - delta, length + delta)
                    a = np.random.uniform(angle - np.pi / 8, angle + np.pi / 8)

                    x = l * np.cos(a)
                    y = l * np.sin(a)

                    self.ax.scatter(
                        x,
                        y,
                        color=self.colors[color_num],
                        marker=self.markers[i],
                        alpha=0.5,
                        linewidths=0.25,
                    )

    def draw_circles(self):
        """Draw the domain of the weird science beings"""
        angle = np.linspace(0, 2 * np.pi, 250)

        for i in range(self.num_circles):
            radius = (i + 1) * self.stratum_radii

            x = radius * np.cos(angle)
            y = radius * np.sin(angle)

            # draw a circle
            self.ax.plot(x, y, color="gray")

    def draw(self):
        """Draw everyting for this realm map"""
        self.draw_circles()
        self.generate_points()


def main():
    realm_map = RealmMap(title="The world of Weird Science Beings")
    realm_map.draw()
    realm_map.save()

    print("Drawing Complete")


if __name__ == "__main__":
    main()
