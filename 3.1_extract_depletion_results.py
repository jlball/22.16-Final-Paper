import openmc.deplete
import matplotlib.pyplot as plt

results = openmc.deplete.ResultsList.from_hdf5("depletion_results.h5")

times, Pu_atoms = results.get_atoms("4", 'Pu239')
_, U_atoms = results.get_atoms("4", 'U238')
_, Li_atoms = results.get_atoms("4", 'Li6')

fig, ax = plt.subplots()
ax.plot(times, Pu_atoms)
ax.plot(times, U_atoms)
ax.plot(times, Li_atoms)

ax.set(xlabel='time (s)', ylabel='Number of atoms',
       title='Build up of Pu-239')
ax.grid()
plt.savefig('atoms.png')
plt.show()

