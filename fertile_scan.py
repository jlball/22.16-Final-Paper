import math
import numpy as np
import openmc
import openmc_data_downloader as odd
import neutronics_material_maker as nmm

mat_plasma = openmc.Material(name="plasma")
mat_plasma.add_element("H", 1, "ao")
mat_plasma.set_density("g/cm3", 0.00001)

# Use of Inconel-718 superalloy comes from 2015 ARC paper
#inconel = nmm.Material.from_library('Inconel-718')
#mat_first_wall = inconel.openmc_material
#mat_first_wall.name = 'first_wall'

#Blanket is taken to be a mixture of UF4 and FLiBe
flibe = openmc.Material(name='flibe')
flibe.add_elements_from_formula("BeLi2F4") #Taken from https://en.wikipedia.org/wiki/FLiBe
flibe.set_density("g/cm3", 1.94)

uf4 = openmc.Material(name='uf4')
uf4.add_elements_from_formula('UF4') # Taken from https://en.wikipedia.org/wiki/Uranium_tetrafluoride
uf4.set_density("g/cm3", 6.7)

mat_inboard_blanket = openmc.Material.mix_materials([flibe, uf4], [95, 5], percent_type='vo', name="inboard_blanket")
mat_outboard_blanket = openmc.Material.mix_materials([flibe, uf4], [95, 5], percent_type='vo', name="outboard_blanket")

mat_vv = openmc.Material(name="vv")
mat_vv.add_element("W", 1, "ao")
mat_vv.set_density("g/cm3", 19.3)


materials = openmc.Materials(
    [
	mat_plasma,
	mat_outboard_blanket,
	mat_inboard_blanket,
	mat_vv,
    ]
)

# downloads the nuclear data and sets the openmc_cross_sections environmental variable
#odd.just_in_time_library_generator(
#    libraries='ENDFB-7.1-NNDC',
#    materials=materials
#)

openmc.Materials.cross_sections = '/home/jlball/Desktop/ENDF VIII.1/endfb80_hdf5/cross_sections.xml' 
