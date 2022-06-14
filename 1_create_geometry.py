import paramak

###
# The geometry herein setup is modeled after the A. Kuang 2018 Fusion Engineering and Design paper on the ARC reactor
# concept. Notably it includes a cooling channel, a solid neutron multiplier layer, and an outer vacuum vessel.
#
# Developed by John Ball in 2022
###


# all units in degrees
inboard_angle_offset = 5
outboard_angle_offset = 12

# all units in cm
plasma_offset = 10

#Whether or not a TBR>1 can be achieved is highly dependent on VV thickness and material
vv_thickness = 2
first_wall_thickness = 1
inboard_blanket_thickness = 100
outboard_blanket_thickness = 120
rotation_angle = 180
num_points = 200

#Cooling channel:
cc_thickness = 2

#Multiplier:
mult_thickness = 1

#Outer VV:
outer_vv_thickness = 3

# Colors:
plasma_c = [0.94, 0.012, 1]
tank_c = [0.01176, 0.988, 0.776]
cc_c = tank_c
mult_c = [1, 0, 0]
vv_c = [0.4, 0.4, 0.4]
outer_vv_c = vv_c


plasma = paramak.Plasma(
   major_radius=330,
   minor_radius= 113,
   triangularity=0.33,
   elongation=1.84,
   rotation_angle=rotation_angle,
   name='plasma',
   color=plasma_c
)

### INBOARD BLANKET ###

ib_cooling_channel = paramak.BlanketFP(cc_thickness, 
   90 + inboard_angle_offset,
   270 - inboard_angle_offset, 
   plasma=plasma,
   offset_from_plasma=plasma_offset,
   rotation_angle=rotation_angle,
   name='inboard_cc',
   color=cc_c,
   num_points = num_points
)

ib_multiplier = paramak.BlanketFP(mult_thickness, 
   90 + inboard_angle_offset,
   270 - inboard_angle_offset, 
   plasma=plasma,
   offset_from_plasma=plasma_offset + cc_thickness,
   rotation_angle=rotation_angle,
   name='inboard_multiplier',
   color=mult_c,
   num_points = num_points
)

ib_outer_vv = paramak.BlanketFP(outer_vv_thickness, 
   90 + inboard_angle_offset,
   270 - inboard_angle_offset, 
   plasma=plasma,
   offset_from_plasma=plasma_offset + cc_thickness + mult_thickness,
   rotation_angle=rotation_angle,
   name='inboard_outer_vv',
   color=outer_vv_c,
   num_points = num_points
)

ib_tank = paramak.BlanketFP(inboard_blanket_thickness, 
   90 + inboard_angle_offset,
   270 - inboard_angle_offset, 
   plasma=plasma,
   offset_from_plasma=plasma_offset + cc_thickness + mult_thickness + outer_vv_thickness,
   rotation_angle=rotation_angle,
   name='inboard_tank',
   color=tank_c,
   num_points = num_points
)

### OUTBOARD BLANKET ###

ob_cooling_channel = paramak.BlanketFP(cc_thickness, 
   -90 + outboard_angle_offset,
   90 - outboard_angle_offset, 
   plasma=plasma,
   offset_from_plasma=plasma_offset,
   rotation_angle=rotation_angle,
   name='outboard_cc',
   color=cc_c,
   num_points = num_points
)

ob_multiplier = paramak.BlanketFP(mult_thickness, 
   -90 + outboard_angle_offset,
   90 - outboard_angle_offset, 
   plasma=plasma,
   offset_from_plasma=plasma_offset + cc_thickness,
   rotation_angle=rotation_angle,
   name='outboard_multiplier',
   color=mult_c,
   num_points = num_points
)

ob_outer_vv = paramak.BlanketFP(outer_vv_thickness, 
   -90 + outboard_angle_offset,
   90 - outboard_angle_offset, 
   plasma=plasma,
   offset_from_plasma=plasma_offset + cc_thickness + mult_thickness,
   rotation_angle=rotation_angle,
   name='outboard_outer_vv',
   color=outer_vv_c,
   num_points = num_points
)

ob_tank = paramak.BlanketFP(outboard_blanket_thickness, 
   -90 + outboard_angle_offset,
   90 - outboard_angle_offset, 
   plasma=plasma,
   offset_from_plasma=plasma_offset + cc_thickness + mult_thickness + outer_vv_thickness,
   rotation_angle=rotation_angle,
   name='outboard_tank',
   color=tank_c,
   num_points = num_points
)

vv = paramak.BlanketFP(vv_thickness, 
   -90,
   270, 
   plasma=plasma,
   offset_from_plasma=plasma_offset - vv_thickness - 1,
   rotation_angle=rotation_angle,
   name='vv',
   color=vv_c,
   num_points = num_points
)

first_wall = paramak.BlanketFP(first_wall_thickness, 
   -90,
   270, 
   plasma=plasma,
   offset_from_plasma=plasma_offset - vv_thickness - first_wall_thickness,
   rotation_angle=rotation_angle,
   name='first_wall',
   color=[0.6, 0.6, 0.6],
   num_points = num_points
)

arc_reactor = paramak.Reactor(shapes_and_components = [plasma, vv, ob_cooling_channel, ob_multiplier, ob_outer_vv, ob_tank, ib_cooling_channel, ib_multiplier, ib_outer_vv, ib_tank])

#arc_reactor.export_html_3d('arc_reactor.html')
#arc_reactor.export_html('arc_reactor_2d.html')

#print("inboard volume:", blanket_inboard.volume())
#print("outboard volume:", blanket_outboard.volume())
#print("total volume:", (blanket_inboard.volume() + blanket_outboard.volume())*1e-6)

arc_reactor.export_dagmc_h5m(
   min_mesh_size=5,
   max_mesh_size=20
)

