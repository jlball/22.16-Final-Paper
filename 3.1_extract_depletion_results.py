import openmc.deplete
import matplotlib.pyplot as plt

results = openmc.deplete.ResultsList.from_hdf5("depletion_results.h5")

times, number_of_co60_atoms = results.get_atoms("4", 'Pu239')

fig, ax = plt.subplots()
ax.plot(times, number_of_co60_atoms)

ax.set(xlabel='time (s)', ylabel='Number of atoms',
       title='Build up of Pu-239')
ax.grid()
plt.savefig('atoms.png')
plt.show()

