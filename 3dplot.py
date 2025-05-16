import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_cylinder(diameter, length):
    radius = diameter / 2
    resolution = 50

    z = np.linspace(0, length, resolution)
    theta = np.linspace(0, 2 * np.pi, resolution)
    theta_grid, z_grid = np.meshgrid(theta, z)

    x_grid = radius * np.cos(theta_grid)
    y_grid = radius * np.sin(theta_grid)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.7, color='steelblue')

    ax.set_title(f"Cylinder: diameter={diameter} m, length={length} m")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")

    # Compatible with all versions of matplotlib (fallback for set_box_aspect)
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)
    ax.set_zlim(0, length)

    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    x = 0.15  # Diameter in meters
    y = 1.5   # Length in meters
    plot_cylinder(x, y)
