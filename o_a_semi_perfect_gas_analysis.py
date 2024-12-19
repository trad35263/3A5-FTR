# o_a_semi_perfect_gas_analysis

import cfg
import functions

import numpy as np
import matplotlib.pyplot as plt

T_databook = np.linspace(-100, 800, 10)
cp_databook = [1.01, 1.01, 1.02, 1.03, 1.05, 1.07, 1.1, 1.12, 1.14, 1.16]

T = np.linspace(0, 1200, 200)
medium = 'air'

cp = functions.cp(T, medium)

fig1, ax1 = plt.subplots()

ax1.plot(T, cp, label = 'Quadratic best fit')
ax1.plot(T_databook, cp_databook, label = 'Databook values', linestyle = '', marker = '.', markersize = 8)
plt.xlabel('Temperature (°C)', weight = 'bold')
plt.ylabel('Isobaric Specific Heat Capacity (kJ/kgK)', weight = 'bold')
ax1.grid(linewidth = 1)
plt.legend(loc = 'best')
fig1.set_size_inches(8, 5)

plt.show()