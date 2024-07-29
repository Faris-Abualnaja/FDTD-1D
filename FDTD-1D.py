# FDTD-1D simulation
# Faris Abualnaja
# 2024-07-26

# Imports
import numpy as np
import matplotlib.pyplot as plt

# Define Constants
# Constants
mu_0    = 1.25663706e-6         # Permeability of free space (magnetic constant)
eps_0   = 8.85418782e-12        # Permitivitty of free space (electric constant)
c_0     = 1/np.sqrt(mu_0*eps_0)  # Speed of light in a vacuum (2.99792458e8)
imp_0   = np.sqrt(mu_0/eps_0)    # Impedance of free space
eps     = eps_0                 # Relative permitivitty

# Size of simulation domain in space and time
j_max = 500     # 500 cells
n_max = 2000    # 2000 time stamps

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

#Equations


# Simulation loop
for n in range(n_max):
    # Update magnetic field boundaries
    Hz[j_max - 1] = Hz_prev[j_max - 2]
    # Update magnetic field
    for j in range(j_max-1):
        Hz[j] = Hz_prev[j] + (dt/(mu_0*dy))*(Ex[j+1] - Ex[j])
    
    # Magnetic field source
    # Hz[j_source -1] = Hz[j_source -1] + H0

    # Update electric field boundaries
    Ex[0] = Ex_prev[1]
    # Update electric field
    for j in range(1, j_max):
        Ex[j] = Ex_prev[j] + (dt/(eps*dy))*(Hz[j] - Hz[j-1])

    # Electric field source
    # Ex[j_source] = Ex[j_source] + E0