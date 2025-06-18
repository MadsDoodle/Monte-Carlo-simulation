import numpy as np

def apply_periodic(pos, L):
    return pos % L

def NearestImg(rij, L):
    return rij - L * np.round(rij / L)
