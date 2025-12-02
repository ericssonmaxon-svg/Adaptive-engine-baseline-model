"""
performance_plots.py
Generates all Phase 2 thermodynamic performance plots for the
Baseline 0-D Engine Model.

Author: Maxon Ericsson
Project: Ultra-Lightweight Adaptive Cycle Engine – Phase 2

This script produces:
    • Thrust vs Ambient Temperature
    • Isp vs Ambient Temperature
    • Thrust vs Compressor Pressure Ratio
    • Isp vs Compressor Pressure Ratio

Outputs are saved as high-resolution PNG files in:
    outputs/plots/
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Import engine model
from engine_model import EngineModel


# ============================================================
#  CREATE OUTPUT DIRECTORY
# ============================================================

OUTPUT_DIR = os.path.join("outputs", "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
#  PLOT FUNCTIONS
# ============================================================

def plot_isp_vs_temperature(engine):
    temps = np.linspace(230, 310, 20)
    isps = [engine.run(T, 101325)["specific_impulse_s"] for T in temps]

    plt.figure(figsize=(8, 5))
    plt.plot(temps, isps, linewidth=2, color="purple")
    plt.xlabel("Ambient Temperature (K)")
    plt.ylabel("Specific Impulse (s)")
    plt.title("Isp vs Ambient Temperature")
    plt.grid(True)

    path = os.path.join(OUTPUT_DIR, "isp_vs_temperature.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_thrust_vs_temperature(engine):
    temps = np.linspace(230, 310, 20)
    thrusts = [engine.run(T, 101325)["thrust_N"] for T in temps]

    plt.figure(figsize=(8, 5))
    plt.plot(temps, thrusts, linewidth=2, color="darkblue")
    plt.xlabel("Ambient Temperature (K)")
    plt.ylabel("Thrust (N)")
    plt.title("Thrust vs Ambient Temperature")
    plt.grid(True)

    path = os.path.join(OUTPUT_DIR, "thrust_vs_temperature.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_thrust_vs_pr(engine):
    prs = np.linspace(10, 40, 20)
    thrusts = []

    for PR in prs:
        engine.compressor_PR = PR
        thrusts.append(engine.run(288.15, 101325)["thrust_N"])

    # Reset PR to default
    engine.compressor_PR = 18.0

    plt.figure(figsize=(8, 5))
    plt.plot(prs, thrusts, linewidth=2, color="darkred")
    plt.xlabel("Compressor Pressure Ratio")
    plt.ylabel("Thrust (N)")
    plt.title("Thrust vs Compressor Pressure Ratio")
    plt.grid(True)

    path = os.path.join(OUTPUT_DIR, "thrust_vs_pr.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_isp_vs_pr(engine):
    prs = np.linspace(10, 40, 20)
    isps = []

    for PR in prs:
        engine.compressor_PR = PR
        isps.append(engine.run(288.15, 101325)["specific_impulse_s"])

    engine.compressor_PR = 18.0  # Reset default

    plt.figure(figsize=(8, 5))
    plt.plot(prs, isps, linewidth=2, color="green")
    plt.xlabel("Compressor Pressure Ratio")
    plt.ylabel("Specific Impulse (s)")
    plt.title("Isp vs Compressor Pressure Ratio")
    plt.grid(True)

    path = os.path.join(OUTPUT_DIR, "isp_vs_pr.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


# ============================================================
#  MAIN EXECUTION
# ============================================================

def main():
    print("Generating Phase 2 Performance Plots...")

    engine = EngineModel()

    plot_isp_vs_temperature(engine)
    plot_thrust_vs_temperature(engine)
    plot_thrust_vs_pr(engine)
    plot_isp_vs_pr(engine)

    print(f"All plots saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
