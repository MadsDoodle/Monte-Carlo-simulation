import numpy as np
from .boundary import apply_periodic, NearestImg
from .energy import lj_potential
from config import N, max_disp, beta

def monte_carlo_step(positions, energy, N, L, max_disp, beta, rc):
    i = np.random.randint(N)
    old_pos = positions[i].copy()
    new_pos = old_pos + (np.random.rand(3) - 0.5) * max_disp
    new_pos = apply_periodic(new_pos, L=10.0)

    dE = 0.0
    for j in range(N):
        if j != i:
            rij_old = NearestImg(old_pos - positions[j], L=10.0)
            rij_new = NearestImg(new_pos - positions[j], L=10.0)
            r2_old = sum(rij_old**2)
            r2_new = sum(rij_new**2)
            dE += lj_potential(r2_new) - lj_potential(r2_old)

    accept = False
    if dE < 0.0 or np.random.rand() < np.exp(-beta * dE):
        positions[i] = new_pos
        energy += dE
        accept = True

    return positions, energy, accept
