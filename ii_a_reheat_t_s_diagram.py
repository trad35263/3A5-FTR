# ii_a_reheat_t_s_diagram.py

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

n = 10
N = 2500

pressures = []
temperatures = []
enthalpies = []
entropies = []

intermediate_pressure_ratios = np.arange(turbine_pressure_ratio / n, turbine_pressure_ratio, turbine_pressure_ratio / n)

for p1 in intermediate_pressure_ratios:

    p2 = turbine_pressure_ratio / p1

    functions.compressor(cfg.states[-1], compressor_pressure_ratio, cfg.eta_c_poly, N)
    functions.combustor(cfg.states[-1], cfg.turbine_inlet_temperature, cfg.combustor_pressure_loss, N)
    functions.turbine(cfg.states[-1], p1, cfg.eta_t_poly, N)
    functions.combustor(cfg.states[-1], cfg.turbine_inlet_temperature, cfg.combustor_pressure_loss, N)
    functions.turbine(cfg.states[-1], cfg.states[-1]['Pressure (bar)'] / cfg.states[0]['Pressure (bar)'], cfg.eta_t_poly, N)

    pressures.append(cfg.datapoints['Pressure (bar)'])
    temperatures.append(cfg.datapoints['Temperature (degC)'])
    enthalpies.append(cfg.datapoints['Enthalpy (kJ/kg)'])
    entropies.append(cfg.datapoints['Entropy (kJ/kgK)'])

    cfg.initialise_states()


# plot T-s diagram

fig1, ax1 = plt.subplots()

ax = ax1

for i in zip(entropies, temperatures, intermediate_pressure_ratios):
    ax.plot(i[0], i[1], label = 'p1 = ' + str(round(i[2], 1)))

plt.xlabel('Specific Entropy (kJ/kgK)', weight = 'bold')
plt.ylabel('Temperature (°C)', weight = 'bold')
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig1.set_size_inches(8, 5)

plt.show()

# plot p-h diagram

fig2, ax2 = plt.subplots()

ax = ax2

for i in zip(enthalpies, pressures, intermediate_pressure_ratios):
    ax.plot(i[0], i[1], label = 'p1 = ' + str(round(i[2], 1)))

plt.xlabel('Specific Enthalpy (kJ/kg)', weight = 'bold')
plt.ylabel('Pressure (bar)', weight = 'bold')
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig2.set_size_inches(8, 5)

plt.show()

cfg.initialise_states()