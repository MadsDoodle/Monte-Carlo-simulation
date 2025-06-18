from config import N, L, n_steps, save_every
from simulation.setup import initialize_positions_no_overlap
from simulation.energy import total_energy
from simulation.monte_carlo import monte_carlo_step
from simulation.visualisation import plot_energy
import numpy as np

positions = initialize_positions_no_overlap(N, L)
energy = total_energy(positions)
trajectory = []
energies = []

accepted_moves = 0
total_moves = 0

for step in range(n_steps):
    positions, energy, accepted = monte_carlo_step(positions, energy)
    total_moves += 1
    if accepted:
        accepted_moves += 1
    if step % save_every == 0:
        trajectory.append(positions.copy())
        energies.append(energy)

acceptance_ratio = accepted_moves / total_moves
print(f"Acceptance Ratio: {acceptance_ratio:.3f}")

# Save results
np.save("results/trajectory.npy", np.array(trajectory))
np.save("results/energies.npy", np.array(energies))

# Plot
plot_energy(energies, n_steps, save_every)
