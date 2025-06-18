# config.py

import numpy as np

# Simulation box and system
L = 10.0                      # Length of box edge
V = L**3                      # Volume of the cubic box
rho = 0.1                     # Particle number density
N = int(rho * V)              # Number of particles

# Lennard-Jones parameters
rc = 2.5                      # Cutoff radius for interactions

# Simulation control
T = 0.4                       # Temperature
beta = 1.0 / T                # Inverse temperature
n_steps = 20000              # Monte Carlo steps
max_disp = 0.4                # Maximum displacement
save_every = 10               # Save config every N steps

# Reproducibility
SEED = 42
np.random.seed(SEED)
