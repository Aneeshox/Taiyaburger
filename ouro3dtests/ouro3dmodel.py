import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def draw_cylinder(ax, start_z, length, radius, color):
    z = np.linspace(start_z, start_z + length, 30)
    theta = np.linspace(0, 2 * np.pi, 30)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid)
    y_grid = radius * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=0.8)

def draw_cone(ax, start_z, height, base_radius, color):
    z = np.linspace(start_z, start_z + height, 30)
    r = np.linspace(base_radius, 0.001, 30)  # tip radius ~ 0
    theta = np.linspace(0, 2 * np.pi, 30)
    theta_grid, z_grid = np.meshgrid(theta, z)
    r_grid = np.tile(r[:, np.newaxis], (1, 30))
    x_grid = r_grid * np.cos(theta_grid)
    y_grid = r_grid * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=0.8)

def draw_transition(ax, start_z, length, start_radius, end_radius, color):
    z = np.linspace(start_z, start_z + length, 30)
    r = np.linspace(start_radius, end_radius, 30)
    theta = np.linspace(0, 2 * np.pi, 30)
    theta_grid, z_grid = np.meshgrid(theta, z)
    r_grid = np.tile(r[:, np.newaxis], (1, 30))
    x_grid = r_grid * np.cos(theta_grid)
    y_grid = r_grid * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=0.8)

def plot_ouroboros_body():
    fig = plt.figure(figsize=(8, 12))
    ax = fig.add_subplot(111, projection='3d')

    # Define rocket segments (start_z is relative stack height)
    z = 0  # Running z-position

    # Nose cone (approx 0.4572m)
    draw_cone(ax, z, 0.4572, 0.0762, 'red')
    z -= 0.4572

    # Body tubes (ordered top to bottom)
    body_parts = [
        (0.2, 0.0762, 'blue'),      # NoseConeTube
        (0.6096, 0.0762, 'blue'),   # RecoveryTube
        (0.5792, 0.0762, 'blue'),   # AvionicsTube
        (0.0573, 0.0762, 'blue'),   # UpperPVBulkheadTube
    ]
    for length, radius, color in body_parts:
        draw_cylinder(ax, z, length, radius, color)
        z -= length

    # Transition 1: 0.1524 → 0.1337
    draw_transition(ax, z, 0.027, 0.0762, 0.06685, 'gray')
    z -= 0.027

    # Pressure Vessel
    draw_cylinder(ax, z, 1.6602, 0.06685, 'green')
    z -= 1.6602

    # Transition 2: 0.1337 → 0.1726
    draw_transition(ax, z, 0.0843, 0.06685, 0.0863, 'gray')
    z -= 0.0843

    # Fin Can
    draw_cylinder(ax, z, 0.8782, 0.0863, 'blue')
    z -= 0.8782

    # Plot formatting
    ax.set_title("Ouroboros I - Rocket Body")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_xlim(-0.1, 0.1)
    ax.set_ylim(-0.1, 0.1)
    ax.set_zlim(z, 0.1)
    ax.view_init(elev=20, azim=135)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_ouroboros_body()
