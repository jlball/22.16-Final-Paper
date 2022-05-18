import paramak

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


plasma = paramak.Plasma(
   major_radius=330,
   minor_radius= 113,
   triangularity=0.33,
   elongation=1.84,
   rotation_angle=rotation_angle,
   name='plasma',
   color=[0.94, 0.012, 1]
)

blanket_inboard = paramak.BlanketFP(inboard_blanket_thickness, 
   90 + inboard_angle_offset,
   270 - inboard_angle_offset, 
   plasma=plasma,
   offset_from_plasma=plasma_offset,
   rotation_angle=rotation_angle,
   name='inboard_blanket',
   color=[0.01176, 0.988, 0.776],
   num_points = num_points
)

blanket_outboard = paramak.BlanketFP(outboard_blanket_thickness, 
   -90 + outboard_angle_offset,
   90 - outboard_angle_offset, 
   plasma=plasma,
   offset_from_plasma=plasma_offset,
   rotation_angle=rotation_angle,
   name='outboard_blanket',
   color=[0.01176, 0.988, 0.776],
   num_points = num_points
)

vv = paramak.BlanketFP(vv_thickness, 
   -90,
   270, 
   plasma=plasma,
   offset_from_plasma=plasma_offset - vv_thickness - 1,
   rotation_angle=rotation_angle,
   name='vv',
   color=[0.4, 0.4, 0.4],
   num_points = num_points
)

first_wall = paramak.BlanketFP(first_wall_thickness, 
   -90,
   270, 
   plasma=plasma,
   offset_from_plasma=plasma_offset - vv_thickness - first_wall_thickness - 2,
   rotation_angle=rotation_angle,
   name='first_wall',
   color=[0.6, 0.6, 0.6],
   num_points = num_points
)

arc_reactor = paramak.Reactor(shapes_and_components = [plasma, vv, blanket_outboard, blanket_inboard])

arc_reactor.export_html_3d('arc_reactor.html')
arc_reactor.export_html('arc_reactor_2d.html')

print("inboard volume:", blanket_inboard.volume())
print("outboard volume:", blanket_outboard.volume())
print("total volume:", (blanket_inboard.volume() + blanket_outboard.volume())*1e-6)

#arc_reactor.export_dagmc_h5m(
#   volume_atol=1e-6,
#   center_atol=1e-6,
#)

