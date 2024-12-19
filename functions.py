# functions.py

# import modules and config file

import numpy as np
import cfg

# functions to retrieve gas properties

def cp(T, medium):
    if medium == 'air':
        return 7.9e-8 * T**2 + 1.351e-4 * T + 1.006
    else:
        return 1.1


# define functions for turbomachinery components

# compressor

def compressor(state, p_ratio, eta, N):

    T = state['Temperature (degC)']
    h = state['Enthalpy (kJ/kg)']
    s = state['Entropy (kJ/kgK)']

    medium = state['Medium']
    rate = state['Flowrate']

    dp = (state['Pressure (bar)'] * p_ratio - state['Pressure (bar)']) / N

    if p_ratio != 1:

        for p in np.arange(state['Pressure (bar)'], state['Pressure (bar)'] * p_ratio, dp):

            cfg.datapoints['Pressure (bar)'].append(p)
            cfg.datapoints['Temperature (degC)'].append(T)
            cfg.datapoints['Enthalpy (kJ/kg)'].append(h)
            cfg.datapoints['Entropy (kJ/kgK)'].append(s)

            dT = cfg.R * (T + 273.15) * dp / (eta * p * cp(T, medium))      # degC
            T += dT                                             # degC
            h += cp(T, medium) * dT                                     # kJ/kg
            s += cp(T, medium) * dT / (T + 273.15) - cfg.R * dp / p                    # kJ/kgK

    final_state = {}
    final_state['Pressure (bar)'], final_state['Temperature (degC)'], final_state['Enthalpy (kJ/kg)'], final_state['Entropy (kJ/kgK)'], final_state['Medium'], final_state['Flowrate'] = state['Pressure (bar)'] * p_ratio, T, h, s, state['Medium'], state['Flowrate']
    cfg.states.append(final_state)

    cfg.work_totals['Compressor work (kJ/kg)'].append((state['Enthalpy (kJ/kg)'] - h) * rate)

# combustor

def combustor(state, T_output, p_loss, N):

    p_loss *= (T_output - state['Temperature (degC)']) / 600        # ensure larger combustor processes incur greater pressure loss

    p = state['Pressure (bar)']
    h = state['Enthalpy (kJ/kg)']
    s = state['Entropy (kJ/kgK)']

    medium = state['Medium']
    rate = state['Flowrate']

    dT = (T_output - state['Temperature (degC)']) / N

    for T in np.arange(state['Temperature (degC)'], T_output, dT):

        cfg.datapoints['Pressure (bar)'].append(p)
        cfg.datapoints['Temperature (degC)'].append(T)
        cfg.datapoints['Enthalpy (kJ/kg)'].append(h)
        cfg.datapoints['Entropy (kJ/kgK)'].append(s)

        dp = -p_loss * state['Pressure (bar)'] / N          # bar
        p += dp                                             # bar
        h += cp(T, medium) * dT                                     # kJ/kg
        s += cp(T, medium) * dT / (T + 273.15) - cfg.R * dp / p                    # kJ/kgK

    A = (cfg.LCV - cp(T_output, 'combustion products') * (T_output - cfg.T_atm)) / (cp(T_output, 'combustion products') * (T_output - cfg.T_atm) - cp((state['Temperature (degC)'] + T_output) / 2, 'gas') * (state['Temperature (degC)'] - cfg.T_atm))

    final_state = {}
    final_state['Pressure (bar)'], final_state['Temperature (degC)'], final_state['Enthalpy (kJ/kg)'], final_state['Entropy (kJ/kgK)'], final_state['Medium'], final_state['Flowrate'] = p, T, h, s, 'combustion products', state['Flowrate'] * (1 + 1 / A)
    cfg.states.append(final_state)
    
    cfg.work_totals['Combustor heat addition (kJ/kg)'].append(h - state['Enthalpy (kJ/kg)'])

# turbine

def turbine(state, p_ratio, eta, N):

    T = state['Temperature (degC)']
    h = state['Enthalpy (kJ/kg)']
    s = state['Entropy (kJ/kgK)']

    medium = state['Medium']
    rate = state['Flowrate']

    dp = (state['Pressure (bar)'] / p_ratio - state['Pressure (bar)']) / N

    if p_ratio != 1:

        for p in np.arange(state['Pressure (bar)'], state['Pressure (bar)'] / p_ratio, dp):

            cfg.datapoints['Pressure (bar)'].append(p)
            cfg.datapoints['Temperature (degC)'].append(T)
            cfg.datapoints['Enthalpy (kJ/kg)'].append(h)
            cfg.datapoints['Entropy (kJ/kgK)'].append(s)

            dT = eta * cfg.R * (T + 273.15) * dp / (p * cp(T, medium))      # degC
            T += dT                                                         # degC
            h += cp(T, medium) * dT                                         # kJ/kg
            s += cp(T, medium) * dT / (T + 273.15) - cfg.R * dp / p         # kJ/kgK

    final_state = {}
    final_state['Pressure (bar)'], final_state['Temperature (degC)'], final_state['Enthalpy (kJ/kg)'], final_state['Entropy (kJ/kgK)'], final_state['Medium'], final_state['Flowrate'] = state['Pressure (bar)'] / p_ratio, T, h, s, state['Medium'], state['Flowrate']
    cfg.states.append(final_state)
    
    cfg.work_totals['Turbine work (kJ/kg)'].append((state['Enthalpy (kJ/kg)'] - h) * rate)

# exhaust to atmosphere

def exhaust(state, T_exchange, effectiveness, N):
    
    p = state['Pressure (bar)']
    h = state['Enthalpy (kJ/kg)']
    s = state['Entropy (kJ/kgK)']

    medium = state['Medium']
    rate = state['Flowrate']

    T_output = state['Temperature (degC)'] + (T_exchange - state['Temperature (degC)']) * effectiveness

    dT = (T_output - state['Temperature (degC)']) / N

    if dT != 0:
    
        for T in np.arange(state['Temperature (degC)'], T_output, dT):

            cfg.datapoints['Pressure (bar)'].append(p)
            cfg.datapoints['Temperature (degC)'].append(T)
            cfg.datapoints['Enthalpy (kJ/kg)'].append(h)
            cfg.datapoints['Entropy (kJ/kgK)'].append(s)

            h += cp(T, medium) * dT                                   # kJ/kg
            s += cp(T, medium) * dT / (T + 273.15)                    # kJ/kgK

    final_state = {}
    final_state['Pressure (bar)'], final_state['Temperature (degC)'], final_state['Enthalpy (kJ/kg)'], final_state['Entropy (kJ/kgK)'], final_state['Medium'], final_state['Flowrate'] = p, T_output, h, s, state['Medium'], state['Flowrate']
    cfg.states.append(final_state)

# heat exchange in HRSG

def heat_exchanger(state, heat_transferred, N):
    
    p = state['Pressure (bar)']
    T = state['Temperature (degC)']
    h = state['Enthalpy (kJ/kg)']
    s = state['Entropy (kJ/kgK)']

    print(h)

    medium = state['Medium']
    rate = state['Flowrate']

    h_output = h - heat_transferred / rate

    print(h_output)

    dh = (h_output - state['Enthalpy (kJ/kg)']) / N

    print(dh)

    if dh != 0:
    
        for h in np.arange(state['Enthalpy (kJ/kg)'], h_output, dh):

            cfg.datapoints['Pressure (bar)'].append(p)
            cfg.datapoints['Temperature (degC)'].append(T)
            cfg.datapoints['Enthalpy (kJ/kg)'].append(h)
            cfg.datapoints['Entropy (kJ/kgK)'].append(s)

            T += dh / cp(T, medium)                     # degC
            s += dh / (T + 273.15)                    # kJ/kgK

    final_state = {}
    final_state['Pressure (bar)'], final_state['Temperature (degC)'], final_state['Enthalpy (kJ/kg)'], final_state['Entropy (kJ/kgK)'], final_state['Medium'], final_state['Flowrate'] = p, T, h_output, s, state['Medium'], state['Flowrate']
    cfg.states.append(final_state)