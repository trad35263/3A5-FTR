# steam_functions.py

# import modules

import numpy as np
import cfg
import steam_lookup_tables as st


# define functions for turbomachinery components

# feed pump

def feed_pump(state, p_ratio):

    p = state['Pressure (bar)']
    T = state['Temperature (degC)']
    h = state['Enthalpy (kJ/kg)']
    s = state['Entropy (kJ/kgK)']
    v = state['Specific volume (m^3/kg)']

    if p_ratio != 1:

        h += v * (p_ratio - 1) * p * 10**2      # convert p from bar to kPa
        p *= p_ratio

        pp = st.pressure_array[:, 0]

        index = np.interp(p, pp, np.linspace(0, len(pp) - 1, len(pp)))

        h1 = st.enthalpy_array[np.floor(index).astype(np.int64), :]
        h2 = st.enthalpy_array[np.ceil(index).astype(np.int64), :]
        hh = (1 - index % 1) * h1 + index % 1 * h2

        T = np.interp(h, hh, st.temperature_array[0])

    final_state = {}
    final_state['Pressure (bar)'], final_state['Temperature (degC)'], final_state['Enthalpy (kJ/kg)'], final_state['Entropy (kJ/kgK)'], final_state['Specific volume (m^3/kg)'], final_state['Flowrate'] = p, T, h, s, v, state['Flowrate']
    cfg.steam_states.append(final_state)

    cfg.steam_work_totals['Feed pump work (kJ/kg)'].append((state['Enthalpy (kJ/kg)'] - h) * state['Flowrate'])

# boiler

def boiler(state, T_output):

    # up to liquid saturated state

    p = state['Pressure (bar)']

    T = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Temperature (degC)'])
    h = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Liquid specific enthalpy (kJ/kg)'])
    s = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Liquid specific entropy (kJ/kgK)'])
    v = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Liquid specific volume (m^3/kg)'])

    int_state = {}
    int_state['Pressure (bar)'], int_state['Temperature (degC)'], int_state['Enthalpy (kJ/kg)'], int_state['Entropy (kJ/kgK)'], int_state['Specific volume (m^3/kg)'], int_state['Flowrate'] = p, T, h, s, v, state['Flowrate']
    cfg.steam_states.append(int_state)

    # from liquid saturated state to vapour saturated state
    
    h = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Vapour specific enthalpy (kJ/kg)'])
    s = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Vapour specific entropy (kJ/kgK)'])
    v = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Vapour specific volume (m^3/kg)'])

    int_state = {}
    int_state['Pressure (bar)'], int_state['Temperature (degC)'], int_state['Enthalpy (kJ/kg)'], int_state['Entropy (kJ/kgK)'], int_state['Specific volume (m^3/kg)'], int_state['Flowrate'] = p, T, h, s, v, state['Flowrate']
    cfg.steam_states.append(int_state)

    # from vapour saturated state

    T = T_output

    pp = st.pressure_array[:, 0]

    index = np.interp(p, pp, np.linspace(0, len(pp) - 1, len(pp)))

    h1 = st.enthalpy_array[np.floor(index).astype(np.int64), :]
    h2 = st.enthalpy_array[np.ceil(index).astype(np.int64), :]
    hh = (1 - index % 1) * h1 + index % 1 * h2

    h = np.interp(T, st.temperature_array[0], hh)

    s1 = st.entropy_array[np.floor(index).astype(np.int64), :]
    s2 = st.entropy_array[np.ceil(index).astype(np.int64), :]
    ss = (1 - index % 1) * s1 + index % 1 * s2

    s = np.interp(T, st.temperature_array[0], ss)

    final_state = {}
    final_state['Pressure (bar)'], final_state['Temperature (degC)'], final_state['Enthalpy (kJ/kg)'], final_state['Entropy (kJ/kgK)'], final_state['Specific volume (m^3/kg)'], final_state['Flowrate'] = p, T, h, s, v, state['Flowrate']
    cfg.steam_states.append(final_state)
    
    cfg.steam_work_totals['Boiler heat addition (kJ/kg)'].append((h - state['Enthalpy (kJ/kg)']) * state['Flowrate'])

# turbine

def turbine(state, p_ratio, eta):

    s = state['Entropy (kJ/kgK)']       # assume isentropic process
    v = state['Specific volume (m^3/kg)']

    p = state['Pressure (bar)'] / p_ratio
    T = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Temperature (degC)'])

    sf = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Liquid specific entropy (kJ/kgK)'])
    sg = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Vapour specific entropy (kJ/kgK)'])

    hf = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Liquid specific enthalpy (kJ/kg)'])
    hg = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Vapour specific enthalpy (kJ/kg)'])

    hs = np.interp(s, np.append(sf, sg), np.append(hf, hg))

    h = state['Enthalpy (kJ/kg)'] - eta * (state['Enthalpy (kJ/kg)'] - hs)

    s = np.interp(h, np.append(hf, hg), np.append(sf, sg))

    final_state = {}
    final_state['Pressure (bar)'], final_state['Temperature (degC)'], final_state['Enthalpy (kJ/kg)'], final_state['Entropy (kJ/kgK)'], final_state['Specific volume (m^3/kg)'], final_state['Flowrate'] = p, T, h, s, v, state['Flowrate']
    cfg.steam_states.append(final_state)

    cfg.steam_work_totals['Turbine work (kJ/kg)'].append((state['Enthalpy (kJ/kg)'] - h) * state['Flowrate'])

# condenser

def condenser(state):

    p = state['Pressure (bar)']
    T = state['Temperature (degC)']

    h = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Liquid specific enthalpy (kJ/kg)'])
    s = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Liquid specific entropy (kJ/kgK)'])
    v = np.interp(p, st.saturation_properties['Pressure (bar)'], st.saturation_properties['Liquid specific volume (m^3/kg)'])

    final_state = {}
    final_state['Pressure (bar)'], final_state['Temperature (degC)'], final_state['Enthalpy (kJ/kg)'], final_state['Entropy (kJ/kgK)'], final_state['Specific volume (m^3/kg)'], final_state['Flowrate'] = p, T, h, s, v, state['Flowrate']
    cfg.steam_states.append(final_state)