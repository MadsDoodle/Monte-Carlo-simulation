# streamlit_app.py

import streamlit as st
import numpy as np
import os
import json
import matplotlib.pyplot as plt

from simulation.setup import initialize_positions_no_overlap
from simulation.energy import total_energy
from simulation.monte_carlo import monte_carlo_step
from utils.logger import setup_logger

st.set_page_config(page_title="Monte Carlo Molecular Sim", layout="wide")
st.title("🧪 Monte Carlo Simulation (Metropolis Algorithm)")

# Create results directory
os.makedirs("results", exist_ok=True)

# Setup logger
logger = setup_logger(log_file="results/sim.log")
logger.info("Streamlit app started.")

# Sidebar inputs
with st.sidebar:
    st.header("Simulation Configurations")

    L = st.slider("Box Size (L)", 5.0, 20.0, 10.0, 0.5)
    T = st.slider("Temperature (T)", 0.1, 5.0, 0.4, 0.1)
    rho = st.slider("Density (rho)", 0.01, 1.0, 0.1, 0.01)
    n_steps = st.number_input("MC Steps", value=5000, step=500)
    max_disp = st.slider("Max Displacement", 0.01, 1.0, 0.4, 0.01)
    save_every = st.number_input("Save Every N Steps", value=10, step=1)

    if st.button("🧹 Clear Previous Results"):
        for f in os.listdir("results"):
            os.remove(os.path.join("results", f))
        st.sidebar.success("Old results cleared.")

    run_simulation = st.button("🚀 Run Simulation")

# Derived values
V = L**3
N = int(rho * V)
beta = 1.0 / T
rc = 2.5
np.random.seed(42)

if run_simulation:
    st.subheader("🔄 Running Simulation...")
    logger.info("Simulation started.")

    positions = initialize_positions_no_overlap(N, L)
    energy = total_energy(positions)

    trajectory = []
    energies = []
    accepted_moves = 0
    total_moves = 0

    progress = st.progress(0)
    status = st.empty()

    for step in range(n_steps):
        positions, energy, accepted = monte_carlo_step(positions, energy, N, L, max_disp, beta, rc)
        total_moves += 1
        if accepted:
            accepted_moves += 1
        if step % save_every == 0:
            trajectory.append(positions.copy())
            energies.append(energy)
        if step % (n_steps // 100) == 0:
            progress.progress(step / n_steps)
            status.write(f"Step {step} / {n_steps}")

    acceptance_ratio = accepted_moves / total_moves
    logger.info(f"Simulation completed. Acceptance ratio: {acceptance_ratio:.3f}")
    st.success(f"✅ Done! Acceptance Ratio: {acceptance_ratio:.3f}")

    # Save results
    np.save("results/trajectory.npy", np.array(trajectory))
    np.savetxt("results/energies.csv", energies, delimiter=",")
    config = {
        "L": L, "T": T, "rho": rho, "N": N,
        "steps": n_steps, "max_disp": max_disp,
        "save_every": save_every, "rc": rc
    }
    with open("results/config_used.json", "w") as f:
        json.dump(config, f, indent=4)
    logger.info("Saved trajectory, energy, and config.")

    # Plot energy
    st.subheader("📉 Energy vs Monte Carlo Steps")
    fig_energy, ax_energy = plt.subplots()
    ax_energy.plot(range(0, n_steps, save_every), energies, color='blue')
    ax_energy.set_xlabel("MC Steps")
    ax_energy.set_ylabel("Total Energy")
    ax_energy.set_title("Energy over Time")
    ax_energy.grid(True)
    st.pyplot(fig_energy)
    fig_energy.savefig("results/energy_plot.png")

    # Plot 3D snapshot
    st.subheader("📌 Final Particle Positions (3D Snapshot)")
    fig_snap = plt.figure(figsize=(6, 6))
    ax_snap = fig_snap.add_subplot(111, projection='3d')
    x, y, z = trajectory[-1].T
    ax_snap.scatter(x, y, z, alpha=0.7)
    ax_snap.set_xlim([0, L])
    ax_snap.set_ylim([0, L])
    ax_snap.set_zlim([0, L])
    ax_snap.set_title("Final Snapshot")
    st.pyplot(fig_snap)
    fig_snap.savefig("results/final_snapshot.png")

    # Downloads
    st.subheader("📥 Download Results")
    with open("results/energies.csv", "rb") as f:
        st.download_button("📊 Download Energy CSV", f, "energies.csv")

    with open("results/trajectory.npy", "rb") as f:
        st.download_button("📦 Download Trajectory", f, "trajectory.npy")

    with open("results/config_used.json", "rb") as f:
        st.download_button("🧾 Download Config JSON", f, "config_used.json")

    with open("results/energy_plot.png", "rb") as f:
        st.download_button("📉 Download Energy Plot", f, "energy_plot.png")

    with open("results/final_snapshot.png", "rb") as f:
        st.download_button("📌 Download Final Snapshot", f, "final_snapshot.png")

    # Show log
    st.subheader("📝 Simulation Log")
    with open("results/sim.log", "r") as f:
        st.text(f.read())
