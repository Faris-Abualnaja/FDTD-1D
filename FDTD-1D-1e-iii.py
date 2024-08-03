# FDTD-1D with single E-field source
# Adding a material with a different dielectric constant
# Changed frequency from 700 MHz -> 1GHz
# Faris Abualnaja
# 2024-08-03

# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

# Define Constants

# Size of simulation domain in space and time
k_max    = 200 # 200 cells
n_max    = 800 # 400 time stamps
k_source = 5   # Location of source in space (at the 5th cell)

# Constants
mu_0    = 1.25663706e-6         # Permeability of free space (magnetic constant)
eps_0   = 8.85418782e-12        # Permitivitty of free space (electric constant)
c_0     = 1/np.sqrt(mu_0*eps_0) # Speed of light in a vacuum (2.99792458e8)
eps_r   = 4                     # Relative permittivity

# Spatial and temporal step sizes
dy = 0.01       # Step size/cell size in space (y-direction)
dt = dy/(2*c_0) # Step size in time

# Dielectric constant accross material spatial-domain
eps_material    = np.zeros(int(k_max/2))
eps_material[:] = eps_r

# Factor in governing equations as a constant
c = np.ones(k_max)
c[:int(k_max/2)] = 0.5
c[int(k_max/2):] = 0.5/eps_material

# Material across domain: air + some material
material = np.zeros(k_max)
material[:int(k_max/2)] = 0
material[int(k_max/2):] = 1

# Define our electric and magnetic fields (wave propagates in y-direction)
Ex = np.zeros(k_max) # Electric field propagating in the x-direction
Hz = np.zeros(k_max) # Magnetic field propagating in the z-direction

# Define previous states of electric and magnetic fields
Lower_Boundary = np.zeros(n_max) # Electric field propagating in the x-direction
Upper_Boundary = np.zeros(n_max) # Magnetic field propagating in the z-direction

# Electric and magnetic field source
def Source_Function(t):
    # Source parameters: t is an integer, the time step
    freq = 1e9
    w_0  = 2*np.pi*freq

    # Function returns a Gaussian pulse
    return np.sin(w_0*t*dt)

# Setting up figure
fig = plt.figure(figsize=(8,1.75))

# Setting up animation
metadata    = dict(title='FDTD-1D Simulation', artist='Faris-Abualnaja')
writer      = PillowWriter(fps=15, metadata=metadata)

# Simulation and animation creation loop
with writer.saving(fig, 'Gifs/FDTD-1D-1e-iii.gif', 100):
    # Time loop
    for n in range(n_max):
        # Update electric field
        for k in range(1, k_max):
            Ex[k] = Ex[k] + c[k]*(Hz[k-1] - Hz[k])

        # Electric field soft-source
        pulse           = Source_Function(n)
        Ex[k_source]    = pulse + Ex[k_source]

        # Boundary conditions
        Lower_Boundary[n] = Ex[1]
        Upper_Boundary[n] = Ex[k_max-2]

        if n > 1:
            Ex[0]       = Lower_Boundary[n-2]
            Ex[k_max-1] = Upper_Boundary[n-2]
        
        # Update magnetic field
        for k in range(k_max-1):
            Hz[k] = Hz[k] + 0.5*(Ex[k] - Ex[k+1])

        # Plotting
        if n % 5 == 0: # Frame rate
            plt.rcParams['font.size'] = 12
            # Plot the E-field
            plt.plot(Ex, color='b', linewidth=1.5)
            # Plot material
            plt.plot(material, color='k', linewidth=1.5, linestyle='--')
            # Plot parameters
            plt.xlabel('FDTD cells', fontsize='14')
            plt.ylabel('E$_x$', fontsize='14')
            plt.xticks(np.arange(0, 201, step=20))
            plt.xlim(0, 200)
            plt.yticks(np.arange(-1.5, 1.2, step=0.5))
            plt.ylim(-1.2, 1.4)
            plt.text(100, 0.5, 'T = {}'.format(n),
            horizontalalignment='center')
            plt.tight_layout()

            # Capture the plot for creating gif
            writer.grab_frame()
            # Clear figure for next capture
            plt.clf()