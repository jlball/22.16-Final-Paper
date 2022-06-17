import openmc.deplete
import matplotlib.pyplot as plt
import openmc.data as data
import numpy as np

#Converts number of atoms to kg of that isotope
def convert_to_kg(num_atoms, isotope):
    moles = num_atoms / (6.022e23) #divide by avogadro number to get in moles
    mass = (moles * data.atomic_mass(isotope))*0.001 #in kg (atmoic mass is molar mass in units of g/mol)
    return mass

#Retrieve the mass of a particular isotope in the blanket
def get_mass(isotope):
    _, atoms_in = results.get_atoms('4', isotope)
    _, atoms_out = results.get_atoms('5', isotope)

    mass = convert_to_kg(atoms_in + atoms_out, isotope)
    return mass

# Go from a fission rate to a fission power
def get_fis_power(isotope):
    _, fis_rate_in = results.get_reaction_rate("4", isotope, 'fission')
    _, fis_rate_out = results.get_reaction_rate("5", isotope, 'fission')
    power = (fis_rate_in + fis_rate_out) * 200 * 1.602e-13 * 1e-6 #Covert from rate to MW of power
    return power

def plot_results(results):

    results = openmc.deplete.ResultsList.from_hdf5("depletion_results.h5")
    times, _ = results.get_atoms("4", 'Pu239') 

    #List of plutonium isotopes whose masses will be plotted
    plut_isotopes = ['Pu238', 'Pu239', 'Pu240', 'Pu241']

    #List of fissile isotopes whose fission powers will be plotted
    fis_isotopes = ['Pu239', 'Pu241', "U235", 'U238']

    #List of fission products whose masses will be plotted
    fis_products = ['Cs137', 'Sr90', 'Pm147']

    times = times /(365 * 24 * 60 * 60) #Convert to years

    #Extract fission and TBR values from statepoint files
    tbr_std, tbr_vals, fis_std, fis_vals = np.empty(len(times)), np.empty(len(times)), np.empty(len(times)), np.empty(len(times))
    for i in range(0, len(times)):
        sp = openmc.StatePoint(f'openmc_simulation_n{i}.h5')
        
        #Extract TBR values and std dev at each step in the simulation
        tbr_tally = sp.get_tally(name='tbr')
        tbr_vals[i] = tbr_tally.mean
        tbr_std[i] = tbr_tally.std_dev

        #Extract fission rates and std devs from each transport simulation
        fis_tally = sp.get_tally(name='fis')
        fis_vals[i] = fis_tally.mean
        fis_std[i] = fis_tally.std_dev

    #Convert fission tally result to power in megawatts: total source rate (Hz) * energy per fission in MeV * joules/MeV * MW/W
    fis_power = fis_vals * 1.86e20 * 200 * 1.602e-13 * 1e-6 

    ### Plotting ###
    fig, axs = plt.subplots(2, 2)

    #Plot of Plutonium Mass
    for iso in plut_isotopes:
        axs[0, 0].plot(times, get_mass(iso), label=iso)
    axs[0, 0].set(xlabel='time (years)', ylabel='Mass (kg)',
        title='Build up of Plutonium Isotopes in 1 percent Fertile Blanket')
    axs[0, 0].legend()
    axs[0, 0].grid()

    #Plot of fission power
    axs[1, 0].plot(times, fis_power, label='Total Fission Power')
    for iso in fis_isotopes:
        axs[1, 0].plot(times, get_fis_power(iso), label=iso)
    axs[1, 0].set(xlabel='time (years)', ylabel='Power (MW)',
        title='Fission Power in 1 percent Fertile Blanket')
    axs[1, 0].legend()
    axs[1, 0].grid()

    #Plot of Uranium mass
    axs[0, 1].plot(times, get_mass('U238'), label='U238')
    axs[0, 1].set(xlabel='time (years)', ylabel='Mass (kg)',
        title='Mass of U238 in 1 percent Fertile Blanket')
    axs[0, 1].grid()

    #Plot of fission product masses
    for iso in fis_products:
        axs[1, 1].plot(times, get_mass(iso), label=iso)
    axs[1, 1].set(xlabel='time (years)', ylabel='Mass (kg)',
        title='Mass of Certain Fission Products in 1 percent Fertile Blanket')
    axs[1, 1].legend()
    axs[1, 1].grid()

    plt.show()

