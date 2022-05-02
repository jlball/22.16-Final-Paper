import neutronics_material_maker as nmm
all_materials = nmm.AvailableMaterials()

inconel = nmm.Material.from_library('Inconel-718')
