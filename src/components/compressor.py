# compressor.py
# Compressor component for 0-D baseline engine model
# Maxon Ericsson

import math

def compressor(T_in, P_in, pressure_ratio, efficiency):
    """
    Simple ideal compressor model with isentropic efficiency.
    Inputs:
        T_in : inlet temperature (K)
        P_in : inlet pressure (Pa)
        pressure_ratio : compressor pressure ratio (P_out / P_in)
        efficiency : isentropic efficiency (0–1)
    Returns:
        T_out, P_out : outlet temperature and pressure
    """

    gamma = 1.4          # ratio of specific heats for air

    # Ideal isentropic temperature rise
    T_out_isentropic = T_in * pressure_ratio ** ((gamma - 1) / gamma)

    # Real temperature rise with efficiency
    T_out = T_in + (T_out_isentropic - T_in) / efficiency

    # Outlet pressure
    P_out = P_in * pressure_ratio

    return T_out, P_out
