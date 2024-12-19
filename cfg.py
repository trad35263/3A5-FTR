# cfg.py

# import modules and steam lookup tables

import numpy as np
import steam_lookup_tables as st

# gas turbine parameters

turbine_inlet_temperature = 1150    # degC
eta_c_poly = 0.90
eta_t_poly = 0.92
combustor_pressure_loss = 0.05
p_atm = 1.013                       # bar
T_atm = 15                          # degC
R = 0.287                           # kJ/kgK
atm_heat_transfer_effectiveness = 0.9
LCV = 48000 # kJ/kg


# steam cycle parameters

T_cond = 30                             # degC
steam_turbine_inlet_temperature = 550       # degC
eta_t_isen = 0.85
steam_mass_flow_rate = 1 / 8


# store states as dictionaries, diagram datapoints as arrays and work totals for gas turbine cycle

states = []
datapoints = {}
work_totals = {}

def initialise_states():

    initial_state = {}
    initial_state['Pressure (bar)'], initial_state['Temperature (degC)'], initial_state['Enthalpy (kJ/kg)'], initial_state['Entropy (kJ/kgK)'], initial_state['Medium'], initial_state['Flowrate'] = p_atm, T_atm, 0, 0, 'air', 1

    states.clear()
    states.append(initial_state)

    datapoints['Pressure (bar)'], datapoints['Temperature (degC)'], datapoints['Enthalpy (kJ/kg)'], datapoints['Entropy (kJ/kgK)'] = [], [], [], []

    work_totals['Compressor work (kJ/kg)'], work_totals['Turbine work (kJ/kg)'], work_totals['Combustor heat addition (kJ/kg)'] = [], [], []


# store states as dictionaries and work totals for steam cycle

steam_states = []
steam_work_totals = {}

def initialise_steam_states():

    initial_state = {}
    initial_state['Pressure (bar)'] = np.interp(T_cond, st.saturation_properties['Temperature (degC)'], st.saturation_properties['Pressure (bar)'])
    initial_state['Temperature (degC)'] = T_cond
    initial_state['Enthalpy (kJ/kg)'] = np.interp(T_cond, st.saturation_properties['Temperature (degC)'], st.saturation_properties['Liquid specific enthalpy (kJ/kg)'])
    initial_state['Entropy (kJ/kgK)'] = np.interp(T_cond, st.saturation_properties['Temperature (degC)'], st.saturation_properties['Liquid specific entropy (kJ/kgK)'])
    initial_state['Specific volume (m^3/kg)'] = np.interp(T_cond, st.saturation_properties['Temperature (degC)'], st.saturation_properties['Liquid specific volume (m^3/kg)'])
    initial_state['Flowrate'] =steam_mass_flow_rate

    steam_states.clear()
    steam_states.append(initial_state)

    steam_work_totals['Feed pump work (kJ/kg)'], steam_work_totals['Turbine work (kJ/kg)'], steam_work_totals['Boiler heat addition (kJ/kg)'] = [], [], []

# initialise state tables

initialise_states()
initialise_steam_states()