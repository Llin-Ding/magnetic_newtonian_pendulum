from physical_entity import Entity
import numpy as np
import csv
from get_force import get_ac_gravity, get_force_at_distance
t = 0
dt = 0.05 
steps = 1000

in_pos_A = [0,0,0]
in_pos_B = [0.01,0,0]

in_vel_A = [0,0,0]
in_vel_B = [0,0,0]

magnet_A = Entity(mass=0.2, initial_position=in_pos_A)
magnet_B = Entity(mass=0.2, initial_position=in_pos_B)





with open('simulation_results.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
 
    writer.writerow(['Time_s', 'A_x', 'A_y', 'A_z', 'B_x', 'B_y', 'B_z'])
    
   
    for step in range(steps):
        
      
        force_on_B = get_force_at_distance(magnet_B, magnet_A) 
        force_on_A = -force_on_B 
        
        gravity_A = get_ac_gravity(magnet_A)
        gravity_B = get_ac_gravity(magnet_B)
        
       
        magnet_A.apply_force(force_on_A + gravity_A)
        magnet_B.apply_force(force_on_B + gravity_B)
        
        A_x, A_y, A_z = magnet_A.position
        B_x, B_y, B_z = magnet_B.position
        
        
        writer.writerow([t, A_x, A_y, A_z, B_x, B_y, B_z])
        
        
        magnet_A.update(dt)
        magnet_B.update(dt)

        
        if step % 10 == 0:
            print(f"Step {step:3d} | 时间: {t:.2f}s | A位置: [{A_x:.4f}, {A_y:.4f}, {A_z:.4f}]")

        t += dt