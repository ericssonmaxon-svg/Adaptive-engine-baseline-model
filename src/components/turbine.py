# turbine.py
# Turbine component for 0-D baseline engine model
# Maxon Ericsson

def turbine(T_in, P_in, work_required, efficiency):
    """
    Simple turbine model that extracts enough work to drive the compressor.
    Inputs:
        T_in : turbine inlet temperature (K)
        P_in : turbine inlet pressure (Pa)
        work_required : work needed to run the compressor (J/kg)
        efficiency : turbine isentropic efficiency (0–1)
    Returns:
        T_out, P_out : turbine outlet temperature and pressure
    """

    cp = 1005      # J/kg-K (approx for air)
    gamma = 1.33   # typical for hot turbine gas

    # Ideal isentropic temperature drop needed
    delta_T_isentropic = work_required / cp

    # Actual temperature drop considering efficiency
    delta_T_real = delta_T_isentropic / efficiency

    T_out = T_in - delta_T_real

    # Prevent going below physical values
    if T_out < 300:
        T_out = 300

    # Pressure drop based on isentropic relation
    P_ratio = (T_out / T_in) ** (gamma / (gamma - 1))
    P_out = P_in * P_ratio

    return T_out, P_out
