# combustor.py
# Combustor component for 0-D baseline engine model
# Maxon Ericsson

def combustor(T_in, P_in, fuel_air_ratio, combustion_efficiency=0.99, pressure_loss_factor=0.03):
    """
    Simple combustor model that adds heat via fuel and applies pressure loss.
    Inputs:
        T_in : inlet temperature (K)
        P_in : inlet pressure (Pa)
        fuel_air_ratio : fuel-to-air mass ratio
        combustion_efficiency : fraction of fuel energy released
        pressure_loss_factor : fractional pressure drop across combustor
    Returns:
        T_out, P_out : outlet temperature and pressure
    """

    # Heat of combustion for Jet-A fuel (approx)
    LHV = 43e6  # J/kg fuel

    cp = 1005   # J/kg-K (approx for air)

    # Temperature rise from combustion
    delta_T = combustion_efficiency * fuel_air_ratio * LHV / cp

    T_out = T_in + delta_T

    # Pressure loss across combustor
    P_out = P_in * (1 - pressure_loss_factor)

    return T_out, P_out
