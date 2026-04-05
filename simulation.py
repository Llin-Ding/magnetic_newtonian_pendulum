from physical_entity import Entity
import numpy as np
import csv


dt = 0.001  
steps = 1000

in_pos_A = [0,0,0]
in_pos_B = [0.01,0,0]

in_vel_A = [0,0,0]
in_vel_B = [0,0,0]

magnet_A = Entity(mass=0.2, initial_position=in_pos_A)
magnet_B = Entity(mass=0.2, initial_position=in_pos_B)

def get_ac_gravity(entity:Entity,length = 0.14,g = 9.8):

    delta_position = entity.init_pos - entity.position
    F = (entity.mass * g / length) * delta_position


    return F



distances_m = []
forces_N = []

with open('magnetic_force_results.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader) 
    for row in reader:
        if len(row) >= 2:
            distances_m.append(float(row[0]))
            forces_N.append(float(row[1]))


distances_m = np.array(distances_m)
forces_N = np.array(forces_N)


def get_force_at_distance(ent_tar, ent_sou):
    delta_pos = ent_tar.position - ent_sou.position
    distance = np.linalg.norm(delta_pos)

    if distance < 1e-9:
        return np.zeros(3)

    F_mag = np.interp(distance, distances_m, forces_N)
    F = F_mag * delta_pos / distance
    
    return F


for step in range(steps):

    force_on_B = get_force_at_distance(magnet_B, magnet_A) 
    force_on_A = -force_on_B 
    
    gravity_A = get_ac_gravity(magnet_A)
    gravity_B = get_ac_gravity(magnet_B)
    

    magnet_A.apply_force(force_on_A + gravity_A)
    magnet_B.apply_force(force_on_B + gravity_B)
    

    magnet_A.update(dt)
    magnet_B.update(dt)


    if step % 10 == 0:
        print(f"Step {step:3d} | A位置: {magnet_A.position} | B位置: {magnet_B.position}")