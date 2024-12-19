# iii_b_steam_cycle_optimisation

# import packages

import numpy as np
import matplotlib.pyplot as plt

import cfg
import steam_functions
import steam_lookup_tables as st


# variables

n = 500

steam_pressure_ratio_max = 3000
steam_pressure_ratios = np.linspace(300, steam_pressure_ratio_max, n)

work_outputs = []
efficiencies = []

for p in steam_pressure_ratios:

    steam_functions.feed_pump(cfg.steam_states[-1], p)
    steam_functions.boiler(cfg.steam_states[-1], cfg.steam_turbine_inlet_temperature)
    steam_functions.turbine(cfg.steam_states[-1], p, cfg.eta_t_isen)
    steam_functions.condenser(cfg.steam_states[-1])

    work_outputs.append(sum(cfg.steam_work_totals['Feed pump work (kJ/kg)']) + sum(cfg.steam_work_totals['Turbine work (kJ/kg)']))
    efficiencies.append((sum(cfg.steam_work_totals['Feed pump work (kJ/kg)']) + sum(cfg.steam_work_totals['Turbine work (kJ/kg)'])) / sum(cfg.steam_work_totals['Boiler heat addition (kJ/kg)']))

    cfg.initialise_steam_states()

fig1, ax1 = plt.subplots()

ax = ax1

plt.plot(steam_pressure_ratios, np.asarray(efficiencies) * 100)

plt.xlabel('Steam Pressure Ratio', weight = 'bold')
plt.ylabel('Thermal efficiency (%)', weight = 'bold')
ax.grid(linewidth = 1)
fig1.set_size_inches(8, 5)

plt.show()

print('Optimum fractional pressure ratio is ' + str(steam_pressure_ratios[np.argmax(efficiencies)]) + ' to optimise thermal efficiency at ' + str(max(efficiencies)))

fig2, ax2 = plt.subplots()

ax = ax2

plt.plot(steam_pressure_ratios, work_outputs)

plt.xlabel('Steam Pressure Ratio', weight = 'bold')
plt.ylabel('Specific Work Output (kJ/kg)', weight = 'bold')
ax.grid(linewidth = 1)
fig2.set_size_inches(8, 5)

plt.show()

print('Optimum fractional pressure ratio is ' + str(steam_pressure_ratios[np.argmax(work_outputs)]) + ' to optimise specific work output at ' + str(max(work_outputs)))