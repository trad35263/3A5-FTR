# o_b_example_T_s_diagram.py

# import packages

import numpy as np
import matplotlib.pyplot as plt

import cfg
import functions


# variables

compressor_pressure_ratio = 30


# calculated values

turbine_pressure_ratio = compressor_pressure_ratio * (1 - cfg.combustor_pressure_loss)


# create gas turbine cycle to investigate effect of intercooler pressure ratio

N = 2500

functions.compressor(cfg.states[-1], compressor_pressure_ratio, cfg.eta_c_poly, N)
functions.combustor(cfg.states[-1], cfg.turbine_inlet_temperature, cfg.combustor_pressure_loss, N)
functions.turbine(cfg.states[-1], turbine_pressure_ratio, cfg.eta_t_poly, N)

pressures = cfg.datapoints['Pressure (bar)']
temperatures = cfg.datapoints['Temperature (degC)']
enthalpies = cfg.datapoints['Enthalpy (kJ/kg)']
entropies = cfg.datapoints['Entropy (kJ/kgK)']

w = sum(cfg.work_totals['Compressor work (kJ/kg)']) + sum(cfg.work_totals['Turbine work (kJ/kg)'])
eta = w / sum(cfg.work_totals['Combustor heat addition (kJ/kg)'])

fig1, ax1 = plt.subplots()

ax = ax1

ax.plot(entropies, temperatures, label = 'Basic Cycle\nWork output: ' + str(np.round(w, 1)) + 'kJ/kg\nThermal efficiency: ' + str(np.round(eta, 3)) + '\nPressure ratio: ' + str(compressor_pressure_ratio))

plt.xlabel('Specific Entropy (kJ/kgK)', weight = 'bold')
plt.ylabel('Temperature (°C)', weight = 'bold')
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig1.set_size_inches(8, 5)

plt.show()

fig2, ax2 = plt.subplots()

ax = ax2

ax.plot(enthalpies, pressures, label = 'Basic Cycle\nWork output: ' + str(np.round(w, 1)) + 'kJ/kg\nThermal efficiency: ' + str(np.round(eta, 3)) + '\nPressure ratio: ' + str(compressor_pressure_ratio))

plt.xlabel('Specific Enthalpy (kJ/kg)', weight = 'bold')
plt.ylabel('Pressure (bar)', weight = 'bold')
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig2.set_size_inches(8, 5)

plt.show()

cfg.initialise_states()