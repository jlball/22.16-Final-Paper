import openmc
import openmc.deplete
from simple_openmc_depletion import create_openmc_model
from extract_simple_depletion_results import plot_results

###
# This script 

#Open the DAGMC geometry of choice for the model to pass to the create_openmc_model function
dag_univ = openmc.DAGMCUniverse("dagmc.h5m")

#Use the create_openmc_model function to create a model with the desired geometry and fertile blanket percent
model = create_openmc_model(1, dag_univ, 10, 1000)

#Open the chain file which contains all of the decay data needed for depletion simulations
chain_filename = 'chain_endfb71.xml'
chain = openmc.deplete.Chain.from_xml(chain_filename)

#Use this model to create a transport operator for use in a depletion simulation
operator = openmc.deplete.Operator(model, chain_filename, normalization_mode='source-rate')

#Set the timesteps and source rates to use for the depletion simulation
time_steps = [1000000*60*60] * 10
source_rates = [1.86e20]* 10

#Run the depletion simulation using a integration algorithm of choice
integrator = openmc.deplete.PredictorIntegrator(
    operator=operator, timesteps=time_steps, source_rates=source_rates, 
)
#integrator.integrate()

#Load the results from the depletion simulation
results = openmc.deplete.ResultsList.from_hdf5("depletion_results.h5")

#Plot the results from the depletion simulation
plot_results(results)

