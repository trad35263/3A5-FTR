# ii_c_example_cycle_t_s_diagram.py

# import packages

import numpy as np
import matplotlib.pyplot as plt

import cfg
import functions


# variables

compressor_pressure_ratio = 30
p1c = np.sqrt(compressor_pressure_ratio)
p2c = compressor_pressure_ratio / p1c


# calculated values

turbine_pressure_ratio = compressor_pressure_ratio * (1 - cfg.combustor_pressure_loss)
p1t = turbine_pressure_ratio * 0.09
p2t = turbine_pressure_ratio / p1t


# create gas turbine cycle

N = 2500

pressures = []
temperatures = []
enthalpies = []
entropies = []

functions.compressor(cfg.states[-1], p1c, cfg.eta_c_poly, N)
functions.exhaust(cfg.states[-1], cfg.T_atm, cfg.atm_heat_transfer_effectiveness, N)
functions.compressor(cfg.states[-1], p2c, cfg.eta_c_poly, N)
functions.combustor(cfg.states[-1], cfg.turbine_inlet_temperature, cfg.combustor_pressure_loss, N)
functions.turbine(cfg.states[-1], p1t, cfg.eta_t_poly, N)
functions.combustor(cfg.states[-1], cfg.turbine_inlet_temperature, cfg.combustor_pressure_loss, N)
functions.turbine(cfg.states[-1], p2t, cfg.eta_t_poly, N)

pressures.append(cfg.datapoints['Pressure (bar)'])
temperatures.append(cfg.datapoints['Temperature (degC)'])
enthalpies.append(cfg.datapoints['Enthalpy (kJ/kg)'])
entropies.append(cfg.datapoints['Entropy (kJ/kgK)'])

w1 = sum(cfg.work_totals['Compressor work (kJ/kg)']) + sum(cfg.work_totals['Turbine work (kJ/kg)'])
eta1 = w1 / sum(cfg.work_totals['Combustor heat addition (kJ/kg)'])

cfg.initialise_states()

functions.compressor(cfg.states[-1], p1c, cfg.eta_c_poly, N)
functions.exhaust(cfg.states[-1], cfg.T_atm, cfg.atm_heat_transfer_effectiveness, N)
functions.compressor(cfg.states[-1], p2c, cfg.eta_c_poly, N)
functions.combustor(cfg.states[-1], cfg.turbine_inlet_temperature, cfg.combustor_pressure_loss, N)
functions.turbine(cfg.states[-1], cfg.states[-1]['Pressure (bar)'] / cfg.states[0]['Pressure (bar)'], cfg.eta_t_poly, N)

pressures.append(cfg.datapoints['Pressure (bar)'])
temperatures.append(cfg.datapoints['Temperature (degC)'])
enthalpies.append(cfg.datapoints['Enthalpy (kJ/kg)'])
entropies.append(cfg.datapoints['Entropy (kJ/kgK)'])

w2 = sum(cfg.work_totals['Compressor work (kJ/kg)']) + sum(cfg.work_totals['Turbine work (kJ/kg)'])
eta2 = w2 / sum(cfg.work_totals['Combustor heat addition (kJ/kg)'])

cfg.initialise_states()

fig1, ax1 = plt.subplots()

ax = ax1

ax.plot(entropies[0], temperatures[0], label = 'Intercooled and Reheated Cycle\nWork output: ' + str(np.round(w1, 1)) + 'kJ/kg\nThermal efficiency: ' + str(np.round(eta1, 3)) + '\nIntermediate pressure ratio: ' + str(round(p1t, 1)))
ax.plot(entropies[1], temperatures[1], label = 'Intercooled Cycle\nWork output: ' + str(np.round(w2, 1)) + 'kJ/kg\nThermal efficiency: ' + str(np.round(eta2, 3)))

plt.xlabel('Specific Entropy (kJ/kgK)', weight = 'bold')
plt.ylabel('Temperature (°C)', weight = 'bold')
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig1.set_size_inches(8, 5)

plt.show()

fig2, ax2 = plt.subplots()

ax = ax2

ax.plot(enthalpies[0], pressures[0], label = 'Intercooled and Reheated Cycle\nWork output: ' + str(np.round(w1, 1)) + 'kJ/kg\nThermal efficiency: ' + str(np.round(eta1, 3)) + '\nIntermediate pressure ratio: ' + str(round(p1t, 1)))
ax.plot(enthalpies[1], pressures[1], label = 'Intercooled Cycle\nWork output: ' + str(np.round(w2, 1)) + 'kJ/kg\nThermal efficiency: ' + str(np.round(eta2, 3)))

plt.xlabel('Specific Enthalpy (kJ/kg)', weight = 'bold')
plt.ylabel('Pressure (bar)', weight = 'bold')
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig2.set_size_inches(8, 5)

plt.show()