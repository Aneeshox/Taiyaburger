import math

def air_density_exponential(altitude_m):
    """
    Estimate air density using the exponential atmosphere approximation https://en.wikipedia.org/wiki/Density_of_air 
    tested the scale height for best results for ouro in our range of altitudes it will slighly overshoot the heat transfer but should be accurate enough
    """
    rho0 = 1.225     # kg/m³ at sea level
    H = 10075 #10400#10075        # Custom scale height from reference (m) tested for best results
    return rho0 * math.exp(-altitude_m / H)

def air_temperature_from_altitude(altitude_m):
    """
    Estimate air temperature from altitude using a standard lapse rate used wiki formula to get temp from altitude.
    """
    T0 = 288.15      # Sea-level temperature in Kelvin
    L = 0.0065       # Lapse rate for our range in (K/m)
    return T0 - L * altitude_m

def air_viscosity_sutherland(T_K): 
    """
    Calculate dynamic viscosity of air using Sutherland's Law also a wiki find (https://doc.comsol.com/5.5/doc/com.comsol.help.cfd/cfd_ug_fluidflow_high_mach.08.27.html)
    """
    # mu_0 = 1.789e-5  # Reference viscosity (kg/m·s) 
    # T_0 = 288.15     # Reference temp (K) #273
    # C = 110.4        # Sutherland's constant (K) #111
    mu_0 = 1.716e-5  
    T_0 = 273   
    C = 111        
    return mu_0 * (T_K / T_0) ** 1.5 * (T_0 + C) / (T_K + C)

def heat_transfer_coefficient(k_air, diameter, Re, Pr=0.71): #prantl number for air from 0 to 80km so we good for ouro
    """surface heat transfer coefficient"""
    return 0.332 * (k_air / diameter) * (Re ** 0.5) * (Pr ** (1/3))


# === Input values (i used values that are at a maximum velocity for ouro from last year) ===
altitude = 815.5475110127112       # meters
velocity = 327.17125982677516      # m/s
diameter = 0.1525                  # m ( diameter of the av bay)
material_threshold = 198.9 + 273.15  # K (material threshold temperature) # 100°C or 198.9°C depending on grade of epoxy as it is the limiiting fafctor
# === Calculations ===

rho = air_density_exponential(altitude)
T = air_temperature_from_altitude(altitude)
k_air = 0.0257 * (T / 273.15) ** 0.76 #at atmospheric pressuure 
# above is super cooked not sure if it is correct "https://matmake.com/properties/thermal-conductivity-of-air.html","https://www.engineeringtoolbox.com/air-properties-viscosity-conductivity-heat-capacity-d_1509.html"
mu = air_viscosity_sutherland(T)
re = (rho*velocity*diameter)/mu  # Reynolds number s
h = heat_transfer_coefficient(k_air, diameter, re)
q = h * (T - material_threshold)  # Heat transfer rate (W/m²)


print(f"At {altitude:.1f} m high and {velocity:.1f}m/s speed:")
print(f"  Temperature         = {T:.2f} K")
print(f"  Air Density         = {rho:.4f} kg/m³")
print(f"  Dynamic Viscosity   = {mu:.2e} kg/(m·s)")
print(f"  Reynolds Number     = {re:.2f}")
print(f"  Thermal Conductivity = {k_air:.4f} W/(m·K)")
print(f"  Heat Transfer Coef. = {h:.2f} W/(m²·K)")
print(f"  Heat Transfer Rate   = {q:.2f} W/m²")