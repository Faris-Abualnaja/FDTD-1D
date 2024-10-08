# FDTD-1D with single E-field source
# Adding boundary conditions
# Faris Abualnaja
# 2024-08-02

# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

# Define Constants

# Size of simulation domain in space and time
k_max       = 200              # 200 cells
n_max       = 400              # 400 time stamps
k_source    = int(k_max/2)     # Location of source in space (half way)

# Constants
mu_0    = 1.25663706e-6         # Permeability of free space (magnetic constant)
eps_0   = 8.85418782e-12        # Permitivitty of free space (electric constant)
c_0     = 1/np.sqrt(mu_0*eps_0) # Speed of light in a vacuum (2.99792458e8)

# Define our electric and magnetic fields (wave propagates in y-direction)
Ex = np.zeros(k_max) # Electric field propagating in the x-direction
Hz = np.zeros(k_max) # Magnetic field propagating in the z-direction

# Define previous states of electric and magnetic fields
Lower_Boundary = np.zeros(n_max) # Electric field propagating in the x-direction
Upper_Boundary = np.zeros(n_max) # Magnetic field propagating in the z-direction

# Electric and magnetic field source
def Source_Function(t):
    # Source parameters: t is an integer, the time step
    spread  = 12       # Width (300 time steps) of Gaussian pulse
    t_0     = spread*3 # Delay (offset of Gaussian pulse)

    # Function returns a Gaussian pulse
    return np.exp(-0.5 * ((t_0 - t) / spread) ** 2)

# Setting up figure
fig = plt.figure(figsize=(8,3.5))

# Setting up animation
metadata    = dict(title='FDTD-1D Simulation', artist='Faris-Abualnaja')
writer      = PillowWriter(fps=15, metadata=metadata)

# Simulation and animation creation loop
with writer.saving(fig, 'Gifs/FDTD-1D-1c-i.gif', 100):
    # Time loop
    for n in range(n_max):
        # Update electric field
        for k in range(1, k_max):
            Ex[k] = Ex[k] + 0.5*(Hz[k] - Hz[k-1])

        # Electric field source
        pulse           = Source_Function(n)
        Ex[k_source]    = pulse

        # Boundary conditions
        Lower_Boundary[n] = Ex[1]
        Upper_Boundary[n] = Ex[k_max-2]
        if n > 1:
            Ex[0]       = Lower_Boundary[n-2]
            Ex[k_max-1] = Upper_Boundary[n-2]
        
        # Update magnetic field
        for k in range(k_max-1):
            Hz[k] = Hz[k] + 0.5*(Ex[k+1] - Ex[k])

        # Plotting
        if n % 5 == 0: # Frame rate
            plt.rcParams['font.size'] = 12
            # Plot the E-field
            plt.subplot(211)
            plt.plot(Ex, color='b', linewidth=1)
            # Plot parameters
            plt.ylabel('E$_x$', fontsize='14')
            plt.xticks(np.arange(0, 201, step=20))
            plt.xlim(0, 200)
            plt.yticks(np.arange(-1, 1.2, step=1))
            plt.ylim(-1.2, 1.2)
            plt.text(100, 0.5, 'T = {}'.format(n),
            horizontalalignment='center')
            
            # Plot H-field
            plt.subplot(212)
            plt.plot(Hz, color='r', linewidth=1)
            #Plot parameters
            plt.ylabel('H$_y$', fontsize='14')
            plt.xlabel('FDTD cells')
            plt.xticks(np.arange(0, 201, step=20))
            plt.xlim(0, 200)
            plt.yticks(np.arange(-1, 1.2, step=1))
            plt.ylim(-1.2, 1.2)
            plt.subplots_adjust(bottom=0.2, hspace=0.45)
            
            # Capture the plot for creating gif
            writer.grab_frame()
            # Clear figure for next capture
            plt.clf()