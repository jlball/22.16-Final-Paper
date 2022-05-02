import openmc

# open the results file
sp = openmc.StatePoint("statepoint.10.h5")

trit_tally = sp.get_tally(name='tbr')
trit_value = trit_tally.get_values(scores=['(n,Xt)'])
print('trit value:', trit_tally.mean, "+/-", trit_tally.std_dev)

plut_tally = sp.get_tally(name='pbr')
plut_value = plut_tally.get_values(scores=['absorption'])[0][0][0]
print('plut value:', plut_value, "+/-", plut_tally.std_dev)

Be_tally = sp.get_tally(name='Be')
Be_value = Be_tally.get_values(scores=['(n,2n)'])
print('Be value:', Be_value, "+/-", Be_tally.std_dev)

fis_tally = sp.get_tally(name='fis')
fis_value = fis_tally.get_values(scores=['fission'])
print('Fis value:', fis_value, "+/-", fis_tally.std_dev)

#Compute time to significant quantity:
n_rate = 1.86e20 # per second

sig_quantity = 34.34 * 6.02214e23 #Number of thorium nuclei in a significant quantity

breed_rate = n_rate * plut_value

time_to_sq = sig_quantity / breed_rate

print("Time to Pu sig. quantity:", round(time_to_sq, 2), "seconds or", round(time_to_sq/3600, 2), "hours")
