import openmc.deplete
import matplotlib.pyplot as plt

results = openmc.deplete.ResultsList.from_hdf5("depletion_results.h5")

times, Pu_atoms = results.get_atoms("4", 'Pu239') 
_, Pu_atoms_2 = results.get_atoms("5", 'Pu239')
_, U_atoms = results.get_atoms("4", 'U238')
_, Li_atoms = results.get_atoms("4", 'Li7')
_, Te_atoms = results.get_atoms("4", 'Te132')
_, I_atoms = results.get_atoms("4", 'I132')

_, Pu_rxn_rates = results.get_reaction_rate("4", 'Pu239', 'fission')

times = times /(60 * 60) #Convert to hours
Pu_atoms = (Pu_atoms + Pu_atoms_2)/ (33.465 * 6.022e23) #Convert to units of IAEA significant quantity


fig, ax = plt.subplots()
#ax.plot(times, Pu_atoms)
#ax.plot(times, Pu_rxn_rates)
#ax.plot(times, U_atoms)
#ax.plot(times, Li_atoms)
ax.plot(times, Te_atoms)
ax.plot(times, I_atoms)
ax.set_yscale('log')

ax.set(xlabel='time (hrs)', ylabel='Significant Quantities',
       title='Build up of Pu-239 in 1 percent Fertile Blanket')
ax.grid()
plt.show()

