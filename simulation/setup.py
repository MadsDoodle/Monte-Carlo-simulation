import numpy as np
from .boundary import NearestImg

def initialise_positions(N, L):
    return np.random.rand(N, 3) * L

def initialize_positions_no_overlap(N, L, min_dist=0.8):
    positions = []
    while len(positions) < N:
        trial = np.random.rand(3) * L
        if all(np.linalg.norm(NearestImg(trial - np.array(pos), L)) > min_dist for pos in positions):
            positions.append(trial)
    return np.array(positions)
