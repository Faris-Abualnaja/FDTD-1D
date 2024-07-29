# FDTD-1D with Thin Film simulation
# Faris Abualnaja
# 2024-07-26

# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

# Define Constants

# Size of simulation domain in space and time
j_max       = 500               # 500 cells
n_max       = 2000              # 2000 time stamps
j_source    = 10                # Location of source in space (10th cell)

# Constants
mu_0    = 1.25663706e-6         # Permeability of free space (magnetic constant)
eps_0   = 8.85418782e-12        # Permitivitty of free space (electric constant)
c_0     = 1/np.sqrt(mu_0*eps_0) # Speed of light in a vacuum (2.99792458e8)
imp_0   = np.sqrt(mu_0/eps_0)   # Impedance of free space

# Thin Film constants
eps             = np.ones(j_max)*eps_0  # Relative permitivitty throughout domain
eps[250:350]    = 10*eps_0              # Relative permitivitty through thin film

# Material profile and drawing
# If statement, if eps > 0 then make assign
# a value of 1 to the material_profile, else
# the material_profile is 0.
material_profile = eps > eps_0

# Spatial and temporal step sizes
lambda_min  = 400e-9        # Minimum wavelength
dy          = lambda_min/20 # Step size in space (y-direction)
dt          = dy/c_0        # Step size in time

# Define our electric and magnetic fields (wave propagates in y-direction)
Ex = np.zeros(j_max) # Electric field propagating in the x-direction
Hz = np.zeros(j_max) # Magnetic field propagating in the z-direction

# Define previous E- and H-fields
Ex_prev = np.zeros(j_max)
Hz_prev = np.zeros(j_max)

# Electric and magnetic field source
def Source_Function(t):
    # Source parameters
    # t is an integer, the time step
    lambda_0    = 550e-9                    # Centre wavelength of Gaussian pulse
    tau         = 30                        # Width (300 time steps) of Gaussian pulse
    t_0         = tau*3                     # Delay (offset of Gaussian pulse)
    w_0         = (2*np.pi*c_0)/lambda_0    # Centre frequency of Gaussian pulse

    # Function returns a modulated Gaussian
    # dt is used to ensure units are in seconds
    return np.exp(-(t-t_0)**2/tau**2)*np.sin(w_0*t*dt)

# Setting up figure
fig = plt.figure()

# Setting up animation
metadata    = dict(title='FDTD-1D Thin Film Simulation', artist='Faris-Abualnaja')
writer      = PillowWriter(fps=15, metadata=metadata)

# Simulation and animation creation loop
with writer.saving(fig, 'FDTD-1D-Thin-Film.gif', 100):
    for n in range(n_max):
        # Update magnetic field boundaries
        Hz[j_max - 1] = Hz_prev[j_max - 2]
        # Update magnetic field
        for j in range(j_max-1):
            Hz[j] = Hz_prev[j] + (dt/(mu_0*dy))*(Ex[j+1] - Ex[j])
            Hz_prev[j] = Hz[j]
        
        # Magnetic field source
        Hz[j_source-1] -= (1/imp_0)*Source_Function(n)
        Hz_prev[j_source-1] = Hz[j_source-1]

        # Update electric field boundaries
        Ex[0] = Ex_prev[1]
        # Update electric field
        for j in range(1, j_max):
            Ex[j] = Ex_prev[j] + (dt/(eps[j]*dy))*(Hz[j] - Hz[j-1])
            Ex_prev[j] = Ex[j]

        # Electric field source
        Ex[j_source] += Source_Function(n+1)
        Ex_prev[j_source] = Ex[j_source]

        # Plotting
        if n % 10 == 0:
            # Plot the E-field
            plt.plot(Ex)
            # Plot material
            plt.plot(material_profile, 'r')
            # Plot parameters
            plt.ylim([0, 2])
            # Capture the plot for creating gif
            writer.grab_frame()
            # Clear figure for next capture
            plt.cla()