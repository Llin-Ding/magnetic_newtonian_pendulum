from interaction_force import get_force
from get_magnet import get_hollow_cylinder

B_z = 0.63               # 剩磁 (Tesla)
h = 7.3 * 1e-3              # 高度 (m)
r_in = 1.8 * 1e-3           # 内径 (m)
r_out = (7.7 / 2) * 1e-3    # 外径 (m) 
location = (0.01515,0,0)

source_magnet = get_hollow_cylinder(r_in, r_out, h, B_z, location=(0, 0, 0), grid=False)

print(get_force(source_magnet, location, B_z, h, r_in, r_out, delta_m = 0.0001))