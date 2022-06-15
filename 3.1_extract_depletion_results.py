import openmc.deplete
import matplotlib.pyplot as plt
import openmc.data as data
import numpy as np

#Converts number of atoms to kg of that isotope
def convert_to_kg(num_atoms, isotope):
    moles = num_atoms / (6.022e23) #divide by avogadro number to get in moles
    mass = moles * data.atomic_mass(isotope) / 1000 #in kg (atmoic mass is molar mass in units of g/mol)
    return mass

results = openmc.deplete.ResultsList.from_hdf5("depletion_results.h5")

times, Pu_atoms = results.get_atoms("4", 'Pu239') 
_, Pu_atoms_2 = results.get_atoms("5", 'Pu239')
_, U_atoms = results.get_atoms("4", 'U238')
_, Li_atoms = results.get_atoms("4", 'Li7')
_, Te_atoms = results.get_atoms("4", 'Te132')
_, I_atoms = results.get_atoms("4", 'I132')

_, Pu_rxn_rates = results.get_reaction_rate("4", 'Pu239', 'fission')

times = times /(60 * 60) #Convert to hours
Pu_atoms = (Pu_atoms + Pu_atoms_2) #Convert to units of IAEA significant quantity

Pu_mass = convert_to_kg(Pu_atoms, 'Pu239')


fis_vals = np.empty(len(times))
tbr_vals = np.empty(len(times))
tbr_std = np.empty(len(times))
for i in range(0, len(times)):
    sp = openmc.StatePoint(f'openmc_simulation_n{i}.h5')
    
    #Extract TBR values and std dev at each step in the simulation
    tbr_tally = sp.get_tally(name='tbr')
    tbr_vals[i] = tbr_tally.mean
    tbr_std[i] = tbr_tally.std_dev

    fis_tally = sp.get_tally(name='fis')
    fis_vals[i] = fis_tally.mean


fig, ax = plt.subplots()
ax.errorbar(times, tbr_vals, yerr=tbr_std, capsize=4)
#ax.plot(times, Pu_rxn_rates)
#ax.plot(times, U_atoms)
#ax.plot(times, Li_atoms)
#ax.plot(times, Te_atoms)
#ax.plot(times, I_atoms)
#ax.set_yscale('log')

ax.set(xlabel='time (hrs)', ylabel='Mass (kg)',
       title='Build up of Pu-239 in 1 percent Fertile Blanket')
ax.grid()
plt.show()

