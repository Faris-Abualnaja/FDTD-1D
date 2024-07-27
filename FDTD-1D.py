# FDTD-1D simulation
# Faris Abualnaja
# 2024-07-26

# Imports
import numpy as np
import matplotlib.pyplot as plt

# Define Constants
# Constants
u_0     = 1.25663706e-6         # Permeability of free space (magnetic constant)
eps_0   = 8.85418782e-12        # Permitivitty of free space (electric constant)
c_0     = 1/np.sqrt(u_0*eps_0)  # Speed of light in a vacuum (2.99792458e8)
imp_0   = np.sqrt(u_0/eps_0)    # Impedance of free space

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