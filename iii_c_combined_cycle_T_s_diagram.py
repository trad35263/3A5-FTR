# iii_c_combined_cycle_T_s_diagram

# import packages

import numpy as np
import matplotlib.pyplot as plt

import cfg
import functions
import steam_functions
import steam_lookup_tables as st


# variables

steam_pressure_ratio = 1500

compressor_pressure_ratio = 30
p1c = np.sqrt(compressor_pressure_ratio)
p2c = compressor_pressure_ratio / p1c


# calculated values

turbine_pressure_ratio = compressor_pressure_ratio * (1 - cfg.combustor_pressure_loss)
p1t = turbine_pressure_ratio * 0.09
p2t = turbine_pressure_ratio / p1t


# create steam cycle

steam_functions.feed_pump(cfg.steam_states[-1], steam_pressure_ratio)
steam_functions.boiler(cfg.steam_states[-1], cfg.steam_turbine_inlet_temperature)
steam_functions.turbine(cfg.steam_states[-1], steam_pressure_ratio, cfg.eta_t_isen)

# create gas turbine cycle

N = 2500

functions.compressor(cfg.states[-1], p1c, cfg.eta_c_poly, N)
functions.exhaust(cfg.states[-1], cfg.T_atm, cfg.atm_heat_transfer_effectiveness, N)
functions.compressor(cfg.states[-1], p2c, cfg.eta_c_poly, N)
functions.combustor(cfg.states[-1], cfg.turbine_inlet_temperature, cfg.combustor_pressure_loss, N)
functions.turbine(cfg.states[-1], p1t, cfg.eta_t_poly, N)
functions.combustor(cfg.states[-1], cfg.turbine_inlet_temperature, cfg.combustor_pressure_loss, N)
functions.turbine(cfg.states[-1], p2t, cfg.eta_t_poly, N)
functions.heat_exchanger(cfg.states[-1], sum(cfg.steam_work_totals['Boiler heat addition (kJ/kg)']), N)

print(cfg.states)
print(cfg.steam_states)

w1 = sum(cfg.work_totals['Compressor work (kJ/kg)']) + sum(cfg.work_totals['Turbine work (kJ/kg)'])
eta1 = w1 / sum(cfg.work_totals['Combustor heat addition (kJ/kg)'])

gas_pressures = np.array(cfg.datapoints['Pressure (bar)'])
gas_temperatures = np.array(cfg.datapoints['Temperature (degC)'])
gas_enthalpies = np.array(cfg.datapoints['Enthalpy (kJ/kg)'])
gas_entropies = np.array(cfg.datapoints['Entropy (kJ/kgK)'])

w2 = sum(cfg.steam_work_totals['Feed pump work (kJ/kg)']) + sum(cfg.steam_work_totals['Turbine work (kJ/kg)'])
eta2 = w2 / sum(cfg.steam_work_totals['Boiler heat addition (kJ/kg)'])

steam_pressures = np.array(list(map(lambda d: d['Pressure (bar)'], cfg.steam_states)))
steam_temperatures = np.array(list(map(lambda d: d['Temperature (degC)'], cfg.steam_states)))
steam_enthalpies = np.array(list(map(lambda d: d['Enthalpy (kJ/kg)'], cfg.steam_states)))
steam_entropies = np.array(list(map(lambda d: d['Entropy (kJ/kgK)'], cfg.steam_states)))

# align T-s diagrams of gas turbine and steam cycle by pinch point (approximate)

pinch_point_temperature = cfg.steam_states[2]['Temperature (degC)'] + 10
arg = np.argmin(np.flip(np.abs(gas_temperatures - np.ones(len(gas_temperatures)) * pinch_point_temperature)))
pinch_point_correction = gas_entropies[-arg] - cfg.steam_states[2]['Entropy (kJ/kgK)'] * cfg.steam_mass_flow_rate

fig1, ax1 = plt.subplots()

ax = ax1

ax.plot(st.saturation_properties['Liquid specific entropy (kJ/kgK)'] * cfg.steam_mass_flow_rate, st.saturation_properties['Temperature (degC)'], color = 'C4', linewidth = 1, label = 'Vapour Dome')
ax.plot(st.saturation_properties['Vapour specific entropy (kJ/kgK)'] * cfg.steam_mass_flow_rate, st.saturation_properties['Temperature (degC)'], color = 'C4', linewidth = 1)
ax.plot(steam_entropies * cfg.steam_mass_flow_rate, steam_temperatures, label = 'Steam Cycle\nWork output: ' + str(np.round(w2, 1)) + 'kJ/kg\nThermal efficiency: ' + str(np.round(eta2, 3)) + '\nPressure ratio: ' + str(steam_pressure_ratio))

ax.plot(gas_entropies - pinch_point_correction * np.ones(len(gas_temperatures)), gas_temperatures, label = 'Intercooled and reheated cycle\nWork output: ' + str(np.round(w1, 1)) + 'kJ/kg\nThermal efficiency: ' + str(np.round(eta1, 3)))

plt.xlabel('Specific Entropy (kJ/kgK)', weight = 'bold')
plt.ylabel('Temperature (°C)', weight = 'bold')
ax.set_title('Combined cycle work output output: ' + str(round(w1 + w2, 1)) + 'kJ/kg\nCombined cycle required heat addition: ' + str(round(w1 / eta1, 1)) + 'kJ/kg\nCombined cycle thermal efficiency: ' + str(round((w1 + w2) * eta1 / w1, 3)))
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig1.set_size_inches(8, 5)

plt.show()

fig2, ax2 = plt.subplots()

ax = ax2

ax.plot(st.saturation_properties['Liquid specific enthalpy (kJ/kg)'] * cfg.steam_mass_flow_rate, st.saturation_properties['Pressure (bar)'], color = 'C4', linewidth = 1, label = 'Vapour Dome')
ax.plot(st.saturation_properties['Vapour specific enthalpy (kJ/kg)'] * cfg.steam_mass_flow_rate, st.saturation_properties['Pressure (bar)'], color = 'C4', linewidth = 1)
ax.plot(steam_enthalpies * cfg.steam_mass_flow_rate, steam_pressures, label = 'Steam Cycle\nWork output: ' + str(np.round(w2, 1)) + 'kJ/kg\nThermal efficiency: ' + str(np.round(eta2, 3)) + '\nPressure ratio: ' + str(steam_pressure_ratio))

ax.plot(gas_enthalpies, gas_pressures, label = 'Intercooled and reheated cycle\nWork output: ' + str(np.round(w1, 1)) + 'kJ/kg\nThermal efficiency: ' + str(np.round(eta1, 3)))

plt.xlabel('Specific Enthalpy (kJ/kg)', weight = 'bold')
plt.ylabel('Pressure (bar)', weight = 'bold')
plt.ylim(0, 80)
ax.set_title('Combined cycle work output output: ' + str(round(w1 + w2, 1)) + 'kJ/kg\nCombined cycle required heat addition: ' + str(round(w1 / eta1, 1)) + 'kJ/kg\nCombined cycle thermal efficiency: ' + str(round((w1 + w2) * eta1 / w1, 3)))
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig2.set_size_inches(8, 5)

plt.show()

cfg.initialise_states()