import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

percents = [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2, 3, 4, 5]
percents_th = [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2, 3]
time_to_sq_plut = [45297, 9455, 4967, 2220, 1249, 720, 422, 310, 249, 209]
time_to_sq_th = [60632, 12286, 6224, 2595, 1367, 743, 417, 302] #, 241.5, 204]

tbr_plut = [1.0997884, 1.098623, 1.09591, 1.08802, 1.08174761, 1.06867657, 1.051, 1.0336, 1.02028723, 1.00845664]
tbr_th = [1.09759836, 1.09667054, 1.09395836, 1.08903446, 1.07988899, 1.06281687, 1.03542917, 1.01058587, 0.99078083, 0.97021093]


plt.rcParams['text.usetex'] = True

fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(percents, time_to_sq_plut, label=r'$UF_4$', s=20, c='tab:green')
ax.scatter(percents_th, time_to_sq_th, label=r'$ThF_4$', s=20, c='tab:red', marker='x')
#ax.plot(fit_x, fit_y)

ax.set_yscale('log')
ax.set_xlabel(r"Percent $UF_4$ or $ThF_4$ by volume", fontsize=14)
ax.set_ylabel(r"Time to significant quantity (hours)", fontsize=14)
ax.set_title(r"Time to Breed a Significant Quantity of Fissile Material in a FLiBe Blanket with an ARC-like Geometry", fontsize=12)

ax.legend()

plt.hlines(24*365*0.8, 0, 6, colors=['tab:orange'], linestyles="dashed")

plt.hlines(24*30*0.8, 0, 6, colors=['tab:blue'], linestyles="dashed")

txt_offset = 10
ax.text(2, 24*365*0.8 + 500, r"One year with 80 percent uptime", color='tab:orange')
ax.text(2, 24*30*0.8 + 70, r"One month with 80 percent uptime", color='tab:blue')

ax.set_xlim(0, 5.5)
ax.set_ylim(100, 70000)

plt.show()
