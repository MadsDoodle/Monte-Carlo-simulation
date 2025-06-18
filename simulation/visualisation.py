import matplotlib.pyplot as plt

def plot_energy(energies, n_steps, save_every):
    plt.figure(figsize=(6,4))
    plt.plot(range(0, n_steps, save_every), energies)
    plt.xlabel('Steps')
    plt.ylabel('Total Energy')
    plt.title('Energy over Time')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
