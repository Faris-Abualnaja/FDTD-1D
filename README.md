# FDTD-1D
A simulation of an electromagnetic wave propagating through a material in 1-D using a basic FDTD approach.

## File naming system
Each file contains a modified version of the 1D FDTD code. Here is a list of what each file contains:
- FDTD-1D-1a: 1D FDTD simulation with a Gaussian pulse source propagating in free space. The electric field is at whole time steps ($n$, $n + 1$, etc.) and whole space steps ($j$, $j + 1$, etc.), while magnetic field is at half time steps ($n + 1/2$, $n - 1/2$, etc.) and half space steps ($j + 1/2$, $j - 1/2$, etc.).
- FDTD-1D-1b: 1D FDTD simulation with normalised units and a Gaussian pulse source propagating in free space. The electric field is at half time steps ($n + 1/2$, $n - 1/2$, etc.) and half space steps ($j + 1/2$, $j - 1/2$, etc.), while magnetic field is at whole time steps ($n$, $n + 1$, etc.) and whole space steps ($j$, $j + 1$, etc.).
    - FDTD-1D-1b-i: Simulation with no boundary conditions. Fields hit boundary and total reflection occurs.
    - FDTD-1D-1b-ii: Two E-field sources instead of one. Constructive and destructive interference patterns occur.
    - FDTD-1D-1b-iii: Single H-field source instead of E-field source.
    - FDTD-1D-1b-iv: Two H-field sources.
- FDTD-1D-1c: Continuing from FDTD-1D-1b, in these files we look at calculation stability. We alter the factor 0.5 in the update equations to observe its affects.
    - FDTD-1D-1c-i: Changed factor from 0.5 -> 1.0
    - FDTD-1D-1c-ii: Changed factor from 0.5 -> 1.1
    - FDTD-1D-1c-iii: Changed factor from 0.5 -> 0.25
- FDTD-1D-1c: Continuing from FDTD-1D-1c, we now look at boundary conditions and ensure they are absorbing.
    - FDTD-1D-1d-i: At the boundaries the wave propagate through. Introduce previous Ex and Hz variables to assign Ex[0], Ex[max], Hz[0], and Hz[max] values.
