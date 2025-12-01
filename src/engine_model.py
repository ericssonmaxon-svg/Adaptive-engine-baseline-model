"""
engine_model.py
0-D Baseline Turbofan Engine Model (Integrated Component Flow)
Author: Maxon Ericsson
Project: Ultra-Lightweight Adaptive Cycle Engine — Phase 2
"""

# ============================================================
# IMPORTS
# ============================================================

from components.compressor import compressor, compute_compressor_work
from components.combustor import combustor, compute_heat_release
from components.turbine import turbine
from components.nozzle import nozzle, compute_thrust_simple, compute_specific_impulse

from typing import Dict


# ============================================================
# CONSTANTS
# ============================================================

g0 = 9.81       # gravitational acceleration [m/s²]


# ============================================================
# ENGINE MODEL CLASS
# ============================================================

class EngineModel:
    """
    Simple 0-D engine model wrapper.

    Handles:
        • Sequential thermodynamic processing
        • Compressor → Combustor → Turbine → Nozzle
        • Turbine work balance to power compressor
        • Fuel–air ratio calculations
        • Thrust + Isp
    """

    def __init__(
        self,
        mass_flow: float = 50.0,         # kg/s core air flow
        compressor_PR: float = 18.0,     # total pressure ratio
        compressor_eff: float = 0.88,    # compressor efficiency
        turbine_eff: float = 0.90,       # turbine efficiency
        f: float = 0.020                 # baseline fuel–air ratio
    ) -> None:

        self.mass_flow = mass_flow
        self.compressor_PR = compressor_PR
        self.compressor_eff = compressor_eff
        self.turbine_eff = turbine_eff
        self.f = f

    # ============================================================
    # MAIN ENGINE RUN METHOD
    # ============================================================

    def run(self, T_ambient: float, P_ambient: float) -> Dict[str, float]:
        """
        Run the 0-D engine and compute:
            • Station thermodynamic states
            • Thrust
            • Isp
            • Fuel flow

        Returns:
            dict[str, float] of results
        """

        results: Dict[str, float] = {}

        # --------------------------------------------------------
        # 1. COMPRESSOR
        # --------------------------------------------------------
        T2, P2 = compressor(
            T_in=T_ambient,
            P_in=P_ambient,
            pressure_ratio=self.compressor_PR,
            efficiency=self.compressor_eff
        )

        Wc = compute_compressor_work(
            T_in=T_ambient,
            T_out=T2,
            mass_flow=1.0
        )

        # --------------------------------------------------------
        # 2. COMBUSTOR
        # --------------------------------------------------------
        T3, P3 = combustor(
            T_in=T2,
            P_in=P2,
            fuel_air_ratio=self.f
        )

        # --------------------------------------------------------
        # 3. TURBINE (provides compressor shaft work)
        # --------------------------------------------------------
        T4, P4 = turbine(
            T_in=T3,
            P_in=P3,
            work_required=Wc,
            efficiency=self.turbine_eff
        )

        # --------------------------------------------------------
        # 4. NOZZLE → THRUST
        # --------------------------------------------------------
        T5, P5, V5, M5 = nozzle(
            T_in=T4,
            P_in=P4,
            P_ambient=P_ambient
        )

        thrust = compute_thrust_simple(self.mass_flow, V5)
        mdot_fuel = self.mass_flow * self.f
        Isp = compute_specific_impulse(thrust, mdot_fuel)

        # --------------------------------------------------------
        # STORE RESULTS
        # --------------------------------------------------------
        results.update({
            "T2": T2, "P2": P2,
            "T3": T3, "P3": P3,
            "T4": T4, "P4": P4,
            "T5": T5, "P5": P5,

            "V_exit": V5,
            "M_exit": M5,

            "thrust_N": thrust,
            "specific_impulse_s": Isp,
            "fuel_flow_kg_s": mdot_fuel
        })

        return results


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":
    engine = EngineModel()
    out = engine.run(288.15, 101325.0)

    print("\n=== BASELINE ENGINE OUTPUT ===")
    for k, v in out.items():
        print(f"{k:20s} : {v}")
