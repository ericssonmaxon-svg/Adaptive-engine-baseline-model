# nozzle.py
# Nozzle component for 0-D baseline engine model
# Maxon Ericsson

import math

def nozzle(T_in, P_in, P_ambient=101325):
    """
    Simple nozzle model that expands exhaust to ambient pressure.
    Inputs:
        T_in : nozzle inlet temperature (K)
        P_in : nozzle inlet pressure (Pa)
        P_ambient : ambient pressure (Pa)
    Returns:
        V_exit : exhaust velocity (m/s)
        M_exit : exit Mach number
    """

    gamma = 1.4
    R = 287      # J/kg-K
    cp = 1005

    # If nozzle cannot fully expand to ambient, assume choked flow
    if P_in / P_ambient > ((gamma + 1) / 2) ** (gamma / (gamma - 1)):
        # Choked flow condition
        T_exit = T_in * (2 / (gamma + 1))
        V_exit = math.sqrt(gamma * R * T_exit)
        M_exit = 1.0
        return V_exit, M_exit

    # Otherwise, isentropic expansion to ambient pressure
    P_ratio = P_ambient / P_in
    T_exit = T_in * P_ratio ** ((gamma - 1) / gamma)

    # Exit velocity from energy equation
    V_exit = math.sqrt(2 * cp * (T_in - T_exit))

    # Compute Mach number
    a_exit = math.sqrt(gamma * R * T_exit)
    M_exit = V_exit / a_exit

    return V_exit, M_exit
