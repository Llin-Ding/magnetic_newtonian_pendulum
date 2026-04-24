from physical_entity import Entity
import numpy as np
import csv


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


def get_resistance(entity, k_linear=0.000055616, k_quadratic=0.0):
   
    v = entity.velocity
    speed = np.linalg.norm(v)

    if speed < 1e-12:
        return np.zeros(3)

    f_linear = -k_linear * v

   
    f_quadratic = -k_quadratic * speed * v

    return f_linear + f_quadratic