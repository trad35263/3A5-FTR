# ii_b_reheat_optimisation.py

# import packages

import numpy as np
import matplotlib.pyplot as plt

import cfg
import functions


# variables

n1 = 8
n2 = 100
N = 2500

compressor_pressure_ratio_max = 80
compressor_pressure_ratios = np.linspace(10, compressor_pressure_ratio_max, n1)

intercooler_pressures = []
work_outputs = []
efficiencies = []

for p_tot in compressor_pressure_ratios:

    fractional_pressure_ratios = np.linspace(1 / p_tot + 1 / n2, 1 - 1 / n2, n2)
    intercooler_pressures.append(fractional_pressure_ratios)
    
    turbine_pressure_ratio = p_tot * (1 - cfg.combustor_pressure_loss)
    intermediate_pressure_ratios = turbine_pressure_ratio * fractional_pressure_ratios

    eta = []
    w = []

    for p1 in intermediate_pressure_ratios:

        p2 = p_tot / p1

        functions.compressor(cfg.states[-1], p_tot, cfg.eta_c_poly, N)
        functions.combustor(cfg.states[-1], cfg.turbine_inlet_temperature, cfg.combustor_pressure_loss, N)
        functions.turbine(cfg.states[-1], p1, cfg.eta_t_poly, N)
        functions.combustor(cfg.states[-1], cfg.turbine_inlet_temperature, cfg.combustor_pressure_loss, N)
        functions.turbine(cfg.states[-1], p2, cfg.eta_t_poly, N)

        w.append(sum(cfg.work_totals['Compressor work (kJ/kg)']) + sum(cfg.work_totals['Turbine work (kJ/kg)']))
        eta.append((sum(cfg.work_totals['Compressor work (kJ/kg)']) + sum(cfg.work_totals['Turbine work (kJ/kg)'])) / sum(cfg.work_totals['Combustor heat addition (kJ/kg)']))

        cfg.initialise_states()
    
    work_outputs.append(w)
    efficiencies.append(eta)

fig1, ax1 = plt.subplots()

ax = ax1

for i in zip(intercooler_pressures, efficiencies, compressor_pressure_ratios):
    plt.plot(i[0], np.asarray(i[1]) * 100, label = 'PR = ' + str(round(i[2], 1)))

plt.xlabel('Fractional Pressure Ratio', weight = 'bold')
plt.ylabel('Thermal efficiency (%)', weight = 'bold')
plt.xlim(0, 1)
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig1.set_size_inches(8, 5)

plt.show()

print('Optimum fractional pressure ratio is ' + str(intercooler_pressures[2][np.argmax(efficiencies[2])]) + ' to optimise thermal efficiency at ' + str(max(efficiencies[2])))

fig2, ax2 = plt.subplots()

ax = ax2

for i in zip(intercooler_pressures, work_outputs, compressor_pressure_ratios):
    plt.plot(i[0], i[1], label = 'PR = ' + str(round(i[2], 1)))

plt.xlabel('Fractional Pressure Ratio', weight = 'bold')
plt.ylabel('Specific Work Output (kJ/kg)', weight = 'bold')
plt.xlim(0, 1)
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig2.set_size_inches(8, 5)

plt.show()

print('Optimum fractional pressure ratio is ' + str(intercooler_pressures[2][np.argmax(work_outputs[2])]) + ' to optimise specific work output at ' + str(max(work_outputs[2])))

cfg.initialise_states()