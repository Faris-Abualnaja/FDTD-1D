# FDTD-1D
A simulation of an electromagnetic wave propagating through a material in 1-D using a basic FDTD approach.

## File naming system
Each file contains a modified version of the 1D FDTD code. Here is a list of what each file contains:
- FDTD-1D-Test: 1D FDTD simulation with a Gaussian pulse source propagating in free space. The electric field is at whole time steps ($n$, $n + 1$, etc.) and whole space steps ($j$, $j + 1$, etc.), while magnetic field is at half time steps ($n + 1/2$, $n - 1/2$, etc.) and half space steps ($j + 1/2$, $j - 1/2$, etc.).
- FDTD-1D-1a: 1D FDTD simulation with normalised units and a Gaussian pulse source propagating in free space. The electric field is at half time steps ($n + 1/2$, $n - 1/2$, etc.) and half space steps ($j + 1/2$, $j - 1/2$, etc.), while magnetic field is at whole time steps ($n$, $n + 1$, etc.) and whole space steps ($j$, $j + 1$, etc.).
    - FDTD-1D-1a-i: Simulation with no boundary conditions. Fields hit boundary and total reflection occurs.
    - FDTD-1D-1a-ii: Two E-field sources instead of one. Constructive and destructive interference patterns occur.
    - FDTD-1D-1a-iii: Single H-field source instead of E-field source.
    - FDTD-1D-1a-iv: Two H-field sources.
- FDTD-1D-1b: Continuing from FDTD-1D-1a, in these files we look at calculation stability. We alter the factor 0.5 in the update equations to observe its affects.
    - FDTD-1D-1b-i: Changed factor from 0.5 -> 1.0
    - FDTD-1D-1b-ii: Changed factor from 0.5 -> 1.1
    - FDTD-1D-1b-iii: Changed factor from 0.5 -> 0.25
- FDTD-1D-1c: Continuing from FDTD-1D-1c, we now look at boundary conditions and ensure they are absorbing. We also only concentrate on the E-field
    - FDTD-1D-1c-i: At the boundaries the wave propagate through. Introduce previous Ex and Hz variables to assign Ex[0], Ex[max], Hz[0], and Hz[max] values.
    - FDTD-1D-1c-ii: Only displaying E-field and adjusting figure size.
- FDTD-1D-1d: We have now added a dielectric medium half-way through the spatial domain.
    - FDTD-1D-1d-i: Added a dielectric medium with a relative permittivity of 4.
    - FDTD-1D-1d-ii: Fixed the reflection at the end of the dielectric medium (far right side in figure).
    - FDTD-1D-1d-iii: Changed hard source to a soft source so the E-field does not reflect at the source.
- FDTD-1D-1e: Simulating with different sources
    - FDTD-1D-1e-i: Changed source to a sine wave
    - FDTD-1D-1e-ii: Removed absorbing boundary at dielectric end
    - FDTD-1D-1e-iii: Increased frequency to 1GHz
    - FDTD-1D-1e-iv: Increaed frequency to 1.3GHz
    - FDTD-1D-1e-v: Increased frequency to 1.6GHz
    - FDTD-1D-1e-vi: Changed source to a wave packet (modulated gaussian)
