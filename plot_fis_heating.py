import matplotlib.pyplot as plt
import numpy as np

percents = [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2, 3, 4, 5]
th_fis = np.array([8.08027406e-06, 4.0406498e-05, 8.07630681e-05, 0.00020182, 0.00040327, 0.00080539, 0.00160431, 0.00239771, 0.00318313, 0.0039664])

u_fis = np.array([3.83254468e-05, 0.0001917, 0.00038316, 0.00095708, 0.00191122, 0.00381423, 0.00761041, 0.01138316, 0.01516335, 0.01890741])

n_rate = 1.86e20 # per second

th_fis_rate = n_rate * th_fis
u_fis_rate = n_rate * u_fis

fission_energy_in_joules = 3.204e-11 #200 MeV in joules

th_fission_power = th_fis_rate * fission_energy_in_joules
u_fission_power = u_fis_rate * fission_energy_in_joules

plt.rcParams['text.usetex'] = True
fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(percents, th_fission_power/1e6, label=r"$ThF_4$")
ax.scatter(percents, u_fission_power/1e6, label=r'$UF_4$')

ax.legend()

ax.set_ylabel(r'Fission Power in Blanket (MW)', fontsize=14)
ax.set_xlabel(r'Percent $UF_4$ or $ThF_4$ by volume', fontsize=14)
ax.set_title(r'Power from Fission Reactions in a $UF_4$ and $ThF_4$ Doped ARC-like FLiBe Blanket', fontsize=14)

plt.show()

