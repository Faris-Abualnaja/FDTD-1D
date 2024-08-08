# FDTD-1D with single E-field source
# Material is a metallic wall and 
# without specifying dielectric parameters
# Faris Abualnaja
# 2024-08-06

# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

# Define Constants

# Size of simulation domain in space and time
k_max    = 200 # 200 cells
n_max    = 800 # 800 time stamps
k_source = 5   # Location of source in space (at the 5th cell)

# Constants
mu_0    = 1.25663706e-6         # Permeability of free space (magnetic constant)
eps_0   = 8.85418782e-12        # Permitivitty of free space (electric constant)
c_0     = 1/np.sqrt(mu_0*eps_0) # Speed of light in a vacuum (2.99792458e8)
eps_r   = 1                     # Relative permittivity for metal = 1
sigma   = 1e6                   # Very large since it is a metal

# Spatial and temporal step sizes
lambda_     = 550e-9
freq        = 250e6 # (c_0/np.sqrt(eps_r))/lambda_#
lambda_min  = (c_0/np.sqrt(eps_r))/freq
dy          = lambda_min/10             # Step size/cell size in space (y-direction)
dt          = dy/(2*c_0)                # Step size in time

# Dielectric constant accross material spatial-domain
eps_material    = np.zeros(int(k_max/2))
eps_material[:] = eps_r

# Constants in update equation
eaf = (dt*sigma)/(2*eps_r*eps_0)
# Outside material
ca = np.ones(k_max)
# Inside material
ca[int(k_max/2):int(k_max/2)+20] = (1-eaf)/(1+eaf)

cb = np.ones(k_max)
# Outside material
cb[:] = 0.5
# Inside material
cb[int(k_max/2):20] = (1/(2*eps_r*(1+eaf)))

# Material across domain: air + some material
material = np.zeros(k_max)
material[int(k_max/2):int(k_max/2)+25] = 1.5
material = material*2 - 1.5

# Define our electric and magnetic fields (wave propagates in y-direction)
Ex = np.zeros(k_max) # Electric field propagating in the x-direction
Hz = np.zeros(k_max) # Magnetic field propagating in the z-direction

# Define previous states of electric and magnetic fields
# Domain boundaries
Lower_Boundary = np.zeros(n_max) # Electric field propagating in the x-direction
Upper_Boundary = np.zeros(n_max) # Magnetic field propagating in the z-direction
# Material boundaries
Material_Lower_Boundary = np.zeros(n_max)
Material_Upper_Boundary = np.zeros(n_max)

# Electric and magnetic field source
def Source_Function(t, freq):
    # Source parameters: t is an integer, the time step
    w_0  = 2*np.pi*freq

    # Function returns a Gaussian pulse
    return np.sin(w_0*t*dt)

# Setting up figure
fig = plt.figure(figsize=(8,1.75))

# Setting up animation
metadata    = dict(title='FDTD-1D Simulation', artist='Faris-Abualnaja')
writer      = PillowWriter(fps=15, metadata=metadata)

# Simulation and animation creation loop
with writer.saving(fig, 'Gifs/FDTD-1D-1g-iv.gif', 100):
    # Time loop
    for n in range(n_max):
        # Update electric field
        # Metallic wall will reflect, therefore update will be -Ex
        for k in range(1, k_max):
            Ex[k] = Ex[k] + 0.5*(Hz[k] - Hz[k-1])

        # Electric field soft-source
        pulse           = Source_Function(n, freq)
        Ex[k_source]    = pulse + Ex[k_source]

        # Boundary conditions
        Lower_Boundary[n] = Ex[1]
        Upper_Boundary[n] = Ex[k_max-2]

        # Metallic wall perfect electric conductor boundary
        # i.e. complete reflection
        for l in range(int(k_max/2),int(k_max/2)+25):
            Ex[l] = 0

        # Boundaries at beginning and end of domain
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
            plt.plot(Ex, color='b', linewidth=1.5)
            # Plot material
            plt.plot(material, color='k', linewidth=1.5, linestyle='--')
            # Plot parameters
            plt.xlabel('FDTD cells', fontsize='14')
            plt.ylabel('E$_x$', fontsize='14')
            plt.xticks(np.arange(0, 201, step=20))
            plt.xlim(0, 200)
            plt.yticks(np.arange(-2.0, 2.2, step=1.0))
            plt.ylim(-2.2, 2.2)
            plt.text(k_max - 20, -4.5, 'T = {}'.format(n),
            horizontalalignment='center',
            verticalalignment='center'),
            plt.text(k_max - 20, 0.75, '$\epsilon_r$ = {}'.format(eps_r),
            horizontalalignment='center',
            verticalalignment='center'),
            plt.text(k_max - 20, -0.75, '$\sigma$ = {:.2E}'.format(sigma),
            horizontalalignment='center',
            verticalalignment='center')
            plt.tight_layout()

            # Capture the plot for creating gif
            writer.grab_frame()
            # Clear figure for next capture
            plt.clf()