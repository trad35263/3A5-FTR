# iii_a_steam_cycle_T_s_diagram

# import packages

import numpy as np
import matplotlib.pyplot as plt

import cfg
import steam_functions
import steam_lookup_tables as st


# variables
steam_pressure_ratio_max = 3000
n = 10
steam_pressure_ratios = np.linspace(steam_pressure_ratio_max / n,steam_pressure_ratio_max, n)

steam_pressures = []
steam_temperatures = []
steam_enthalpies = []
steam_entropies = []

# create steam cycle

for p in steam_pressure_ratios:

    steam_functions.feed_pump(cfg.steam_states[-1], p)
    steam_functions.boiler(cfg.steam_states[-1], cfg.steam_turbine_inlet_temperature)
    steam_functions.turbine(cfg.steam_states[-1], p, cfg.eta_t_isen)
    steam_functions.condenser(cfg.steam_states[-1])
    
    steam_pressures.append(np.array(list(map(lambda d: d['Pressure (bar)'], cfg.steam_states))))
    steam_temperatures.append(np.array(list(map(lambda d: d['Temperature (degC)'], cfg.steam_states))))
    steam_enthalpies.append(np.array(list(map(lambda d: d['Enthalpy (kJ/kg)'], cfg.steam_states))))
    steam_entropies.append(np.array(list(map(lambda d: d['Entropy (kJ/kgK)'], cfg.steam_states))))

    cfg.initialise_steam_states()

fig1, ax1 = plt.subplots()

ax = ax1

ax.plot(st.saturation_properties['Liquid specific entropy (kJ/kgK)'], st.saturation_properties['Temperature (degC)'], color = 'C4', linewidth = 1, label = 'Vapour Dome')
ax.plot(st.saturation_properties['Vapour specific entropy (kJ/kgK)'], st.saturation_properties['Temperature (degC)'], color = 'C4', linewidth = 1)

for i in zip(steam_entropies, steam_temperatures, steam_pressure_ratios):
    ax.plot(i[0], i[1], label = 'PR = ' + str(round(i[2], 1)))

plt.xlabel('Entropy (kJ/kgK)', weight = 'bold')
plt.ylabel('Temperature (°C)', weight = 'bold')
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig1.set_size_inches(8, 5)

plt.show()

fig2, ax2 = plt.subplots()

ax = ax2

ax.plot(st.saturation_properties['Liquid specific enthalpy (kJ/kg)'], st.saturation_properties['Pressure (bar)'], color = 'C4', linewidth = 1, label = 'Vapour Dome')
ax.plot(st.saturation_properties['Vapour specific enthalpy (kJ/kg)'], st.saturation_properties['Pressure (bar)'], color = 'C4', linewidth = 1)

for i in zip(steam_enthalpies, steam_pressures, steam_pressure_ratios):
    ax.plot(i[0], i[1], label = 'PR = ' + str(round(i[2], 1)))

plt.xlabel('Enthalpy (kJ/kg)', weight = 'bold')
plt.ylabel('Pressure (bar)', weight = 'bold')
ax.legend(loc = 'best')
ax.grid(linewidth = 1)
fig2.set_size_inches(8, 5)

plt.show()