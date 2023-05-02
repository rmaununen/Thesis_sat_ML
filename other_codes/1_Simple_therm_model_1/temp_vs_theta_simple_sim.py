import numpy as np
import matplotlib.pyplot as plt

# Define constants
r_e = 6378.1e3 # radius of Earth (m)
r_orbit = 6378.1e3 + 500e3 # radius of spacecraft's orbit (m)
period = 2 * np.pi * np.sqrt((r_orbit**3) / (3.986e14)) # period of orbit (s)
k = 0.08 # thermal conductivity of spacecraft (W/(m*K))
A = 20 # surface area of spacecraft (m^2)
alpha = 0.75 # solar absorptivity of spacecraft
epsilon = 0.85 # infrared emissivity of spacecraft
sigma = 5.67e-8 # Stefan-Boltzmann constant (W/(m^2*K^4))
d = (1367/4/sigma)**(1/4) # temperature of Earth's radiation (K)
albedo = 0.3 # albedo of Earth

# Define position angles (in radians)
n_theta = 1000
theta = np.linspace(0, 2*np.pi, n_theta)

# Calculate Earth shadow angles as a function of position angle
theta_0 = np.arccos(r_e / r_orbit)
theta_es = 2 * np.arccos(r_e / r_orbit * np.cos(theta) - np.sqrt(1 - (r_e / r_orbit)**2 * np.sin(theta)**2))
theta_ss = 2 * np.arccos(r_e / r_orbit * np.cos(theta) + np.sqrt(1 - (r_e / r_orbit)**2 * np.sin(theta)**2))

# Calculate solar flux at each position angle, taking into account Earth shadowing effect
solar_flux = np.zeros_like(theta)
for i in range(len(theta)):
    if theta[i] < theta_es[i] or theta[i] > theta_ss[i]:
        solar_flux[i] = 0
    elif theta_es[i] <= theta[i] <= theta_ss[i]:
        solar_flux[i] = 1367 * (r_orbit / (149.6e9))**2 / np.cos(theta[i])

# Calculate spacecraft temperature as a function of position angle
T_0 = 273.15 # initial spacecraft temperature (K)
T_max = 2000 # maximum spacecraft temperature (K)
T = np.zeros_like(theta)
T[0] = T_0
dt = period / len(theta) # time step

for i in range(len(theta)-1):
    q_solar = solar_flux[i] * alpha * (1 - albedo) * A # solar heat flux
    q_infrared = epsilon * sigma * A * (-T[i]**4 + d**4) # infrared heat flux
    q_total = q_solar + q_infrared # total heat flux
    dT = q_total * dt / (k * A) # change in temperature
    T[i+1] = T[i] + dT # new temperature

# Plot temperature as a function of position angle
plt.plot(theta, T)
plt.xlabel('Position Angle (rad)')
plt.ylabel('Temperature (K)')
plt.title('Spacecraft Temperature vs Position Angle')
plt.show()

