import math
import numpy as np
import openmc
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

percent_fertile = 5/100

mat_inboard_blanket = openmc.Material.mix_materials([flibe, uf4], [1 - percent_fertile, percent_fertile], percent_type='vo', name="inboard_blanket")
mat_outboard_blanket = openmc.Material.mix_materials([flibe, uf4], [1 - percent_fertile, percent_fertile], percent_type='vo', name="outboard_blanket")

print('density', mat_inboard_blanket.get_mass_density())

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

openmc.Materials.cross_sections = '/home/jlball/downloads/endfb71_hdf5/cross_sections.xml' 

# makes use of the dagmc geometry
dag_univ = openmc.DAGMCUniverse("dagmc.h5m")

# creates an edge of universe boundary surface
vac_surf = openmc.Sphere(r=10000, surface_id=9999, boundary_type="vacuum")

# adds reflective surface for the sector model at 0 degrees
reflective_1 = openmc.Plane(
    a=math.sin(0),
    b=-math.cos(0),
    c=0.0,
    d=0.0,
    surface_id=9991,
    boundary_type="reflective",
)

# specifies the region as below the universe boundary and inside the reflective surfaces
region = -vac_surf & -reflective_1 

# creates a cell from the region and fills the cell with the dagmc geometry
containing_cell = openmc.Cell(cell_id=9999, region=region, fill=dag_univ)

geometry = openmc.Geometry(root=[containing_cell])

# creates a simple isotropic neutron source in the center with 14MeV neutrons
my_source = openmc.Source()
# the distribution of radius is just a single value at the plasma major radius
radius = openmc.stats.Discrete([330.], [1])
# the distribution of source z values is just a single value
z_values = openmc.stats.Discrete([0], [1])
# the distribution of source azimuthal angles values is a uniform distribution between 0 and 0.5 Pi
# these angles must be the same as the reflective angles
angle = openmc.stats.Uniform(a=0., b=math.radians(180))
# this makes the ring source using the three distributions and a radius
my_source.space = openmc.stats.CylindricalIndependent(r=radius, phi=angle, z=z_values, origin=(0.0, 0.0, 0.0))
# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()
# sets the energy distribution to a Muir distribution neutrons
my_source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# specifies the simulation computational intensity
settings = openmc.Settings()
settings.batches = 10
settings.particles = 100000
settings.inactive = 0
settings.run_mode = "fixed source"
settings.source = my_source

# material filter to only study the blanket:
#blanket_filter = openmc.MaterialFilter(mat_blanket)

# Tritium Breeding Tally:
trit_tally = openmc.Tally(name='tbr')
#trit_tally.filters = [blanket_filter]
trit_tally.scores = ["(n,Xt)"]

# Tritium Breeding Tally:
Be_tally = openmc.Tally(name='Be')
#Be_tally.filters = [blanket_filter]
Be_tally.scores = ["(n,2n)"]

# Plutonium Breeding Tally:
plut_tally = openmc.Tally(name='pbr')
plut_tally.nuclides = ['U238']
#plut_tally.filters = [blanket_filter]
plut_tally.scores = ["absorption"]

#Fission tally
fis_tally = openmc.Tally(name='fis')
#fis_tally.filters = [blanket_filter]
fis_tally.scores = ['fission']

tallies = openmc.Tallies([trit_tally, plut_tally, Be_tally, fis_tally])

# builds the openmc model
my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)

# starts the simulation
my_model.run(threads=8)










