import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable, inferno

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
legend_patches = []

# Simulated heat transfer data (W/m²)
heat_data = {
    "NoseCone": 76810,
    "NoseConeTube": 65320,
    "IntermediateTube": 50395,
    "RecoveryTube": 50395,
    "AvionicsTube": 50395,
    "UpperCasing": 50395,
    "UpperTransition": 47921,
    "PVTube": 46694,
    "LowerTransition": 47767,
    "FinCan": 56000,
    "Fins": 32800,
}

norm = Normalize(vmin=min(heat_data.values()), vmax=max(heat_data.values()))
cmap = inferno

def get_color(name):
    return cmap(norm(heat_data[name]))

def tube(name, position, length, diameter):
    r = diameter / 2
    z = np.linspace(position, position - length, 30)
    theta = np.linspace(0, 2 * np.pi, 30)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x = r * np.cos(theta_grid)
    y = r * np.sin(theta_grid)
    ax.plot_surface(x, y, z_grid, color=get_color(name), alpha=0.9)
    legend_patches.append(Patch(facecolor=get_color(name), label=f"{name} - {heat_data[name]:.0f} W/m²"))

def transition(name, position, length, start_d, end_d):
    r1, r2 = start_d / 2, end_d / 2
    z = np.linspace(position, position - length, 30)
    r = np.linspace(r1, r2, 30)
    theta = np.linspace(0, 2 * np.pi, 30)
    theta_grid, z_grid = np.meshgrid(theta, z)
    r_grid = np.tile(r[:, np.newaxis], (1, 30))
    x = r_grid * np.cos(theta_grid)
    y = r_grid * np.sin(theta_grid)
    ax.plot_surface(x, y, z_grid, color=get_color(name), alpha=0.9)
    legend_patches.append(Patch(facecolor=get_color(name), label=f"{name} - {heat_data[name]:.0f} W/m²"))

def add_fins(position, span, root_chord, thickness, radius, num_fins=3):
    angles = np.linspace(0, 2*np.pi, num_fins, endpoint=False)
    color = get_color("Fins")

    for angle in angles:
        profile = np.array([
            [0.0, 0.0],
            [0.2 * root_chord, span],
            [0.5 * root_chord, span],
            [0.8 * root_chord, span],
            [1.0 * root_chord, 0.0],
            [0.0, 0.0]
        ])
        fin_3d = []
        for dz in [0, thickness]:
            for z, r in profile:
                x = (radius + r) * np.cos(angle)
                y = (radius + r) * np.sin(angle)
                fin_3d.append([x, y, position + z + dz])
        N = len(profile)
        faces = [fin_3d[0:N], fin_3d[N:2*N]]
        for i in range(N - 1):
            faces.append([fin_3d[i], fin_3d[i+1], fin_3d[i+1+N], fin_3d[i+N]])
        ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=0.5, alpha=0.9))
    legend_patches.append(Patch(facecolor=color, label=f"Fins - {heat_data['Fins']} W/m²"))

def add_nosecone(position, base_d, aspect_ratio, resolution=100):
    r = base_d / 2
    L = base_d * aspect_ratio
    z = np.linspace(0, L, resolution)
    chord = np.hypot(L, r)
    R = (chord**2) / (2 * r)
    r_profile = np.sqrt(R**2 - (z - L)**2) - (R - r)
    theta = np.linspace(0, 2 * np.pi, resolution)
    theta_grid, z_grid = np.meshgrid(theta, z)
    r_grid = np.tile(r_profile[:, np.newaxis], (1, resolution))
    x = r_grid * np.cos(theta_grid)
    y = r_grid * np.sin(theta_grid)
    ax.plot_surface(x, y, position - z_grid, color=get_color("NoseCone"), alpha=0.9)
    legend_patches.append(Patch(facecolor=get_color("NoseCone"), label=f"NoseCone - {heat_data['NoseCone']} W/m²"))

# Geometry
add_nosecone(0.0, 0.1524, 2.9856)
tube("NoseConeTube", -0.455, 0.238, 0.1524)
tube("IntermediateTube", -0.693, 0.3747, 0.1524)
tube("RecoveryTube", -1.0677, 0.6096, 0.1524)
tube("AvionicsTube", -1.6773, 0.58, 0.1524)
tube("UpperCasing", -2.2573, 0.05715, 0.1524)
transition("UpperTransition", -2.31445, 0.025, 0.1524, 0.142875)
tube("PVTube", -2.33945, 1.66, 0.142875)
transition("LowerTransition", -3.99945, 0.0842772, 0.142875, 0.168)
tube("FinCan", -4.0837, 0.868, 0.168)
add_fins(-4.862, 0.14, 0.36, 0.009906, 0.168 / 2)

# View settings
ax.set_title("Ouroboros I - Thermal Map")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.view_init(elev=20, azim=135)

# Equal scale
x_range = np.ptp(ax.get_xlim3d())
y_range = np.ptp(ax.get_ylim3d())
z_range = np.ptp(ax.get_zlim3d())
max_range = max(x_range, y_range, z_range) / 2
mid_x = np.mean(ax.get_xlim3d())
mid_y = np.mean(ax.get_ylim3d())
mid_z = np.mean(ax.get_zlim3d())
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

# Colorbar
sm = ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, shrink=0.6, pad=0.1)
cbar.set_label("Heat Transfer Rate (W/m²)")

# Legend
ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.show()
