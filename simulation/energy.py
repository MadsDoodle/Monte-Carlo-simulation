from .boundary import NearestImg
from config import rc, N, L

def lj_potential(r2):
    if r2 < rc**2:
        inv_r6 = (1.0 / r2)**3
        return 4 * (inv_r6**2 - inv_r6)
    return 0.0

def total_energy(positions):
    energy = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            rij = NearestImg(positions[i] - positions[j], L)
            r2 = sum(rij ** 2)
            energy += lj_potential(r2)
    return energy
