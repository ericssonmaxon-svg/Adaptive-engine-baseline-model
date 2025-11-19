# engine_model.py
# Baseline 0-D Turbofan Model
# Maxon Ericsson

from components.compressor import compressor
from components.combustor import combustor
from components.turbine import turbine
from components.nozzle import nozzle

import math

def main():
    print("Running baseline 0-D turbofan engine model...\n")

    # ---------------------------------------------------
    # 1. SET ENGINE INPUT PARAMETERS
    # ---------------------------------------------------

    T_ambient = 288.15     # K   (15°C)
    P_ambient = 101325     # Pa  (sea level)

    mass_flow = 50         # kg/s (core mass flow)
    pressure_ratio = 18    # overall compressor ratio
    eta_comp = 0.88        # compressor efficiency
    eta_turb = 0.90        # turbine efficiency

    fuel_air_ratio = 0.02  # baseline F/A ratio
    TIT = 1500             # turbine inlet temp target (K)

    # ---------------------------------------------------
    # 2. COMPRESSOR
    # ---------------------------------------------------

    T2, P2 = compressor(T_ambient, P_ambient, pressure_ratio, eta_comp)
    print(f"Compressor exit: T2={T2:.2f} K, P2={P2/1000:.2f} kPa")

    # ---------------------------------------------------
    # 3. COMBUSTOR
    # ---------------------------------------------------

    T3, P3 = combustor(T2, P2, fuel_air_ratio)
    print(f"Combustor exit: T3={T3:.2f} K, P3={P3/1000:.2f} kPa")

    # ---------------------------------------------------
    # 4. TURBINE WORK REQUIREMENT
    # ---------------------------------------------------

    cp = 1005
    compressor_work = cp * (T2 - T_ambient)
    print(f"Compressor work required: {compressor_work:.2f} J/kg")

    # ---------------------------------------------------
    # 5. TURBINE
    # ---------------------------------------------------

    T4, P4 = turbine(T3, P3, compressor_work, eta_turb)
    print(f"Turbine exit: T4={T4:.2f} K, P4={P4/1000:.2f} kPa")

    # ---------------------------------------------------
    # 6. NOZZLE + EXHAUST VELOCITY
    # ---------------------------------------------------

    V_exit, M_exit = nozzle(T4, P4, P_ambient)
    print(f"Nozzle exit velocity: {V_exit:.2f} m/s (Mach {M_exit:.2f})")

    # ---------------------------------------------------
    # 7. THRUST
    # ---------------------------------------------------

    thrust = mass_flow * V_exit
    print(f"\nNET THRUST: {thrust:.2f} N")


if __name__ == "__main__":
    main()
