from physical_entity import Entity
import numpy as np
import csv
from get_force import get_ac_gravity, get_force_at_distance, get_resistance
t = 0
dt = 0.05 
steps = 10000

in_pos_A = [0, 0, 0]
in_pos_B_start = [0.080, 0, 0]

in_vel_A = [0, 0, 0]
in_vel_B = [0, 0, 0]

# 2. 初始化实体：将质量修改为 2g (即 0.002 kg)
magnet_A = Entity(mass=0.0022, initial_position=in_pos_A, initial_velocity=in_vel_A)
magnet_B = Entity(mass=0.0022, initial_position=in_pos_B_start, initial_velocity=in_vel_B)

# 3. 设定悬挂点(平衡点)：悬挂在 0.059m 处，供重力/回复力函数使用 (必须是 numpy 数组)
magnet_A.init_pos = np.array([0, 0, 0]) # 补充：确保 A 的 init_pos 也是正确的向量格式
magnet_B.init_pos = np.array([0.059, 0, 0])


with open('simulation_results.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
 
    writer.writerow(['Time_s', 'A_x', 'A_y', 'A_z', 'B_x', 'B_y', 'B_z'])
    
   
    for step in range(steps):
        
      
        force_on_B = get_force_at_distance(magnet_B, magnet_A) 
        force_on_A = -force_on_B 
        
        gravity_A = get_ac_gravity(magnet_A)
        gravity_B = get_ac_gravity(magnet_B)
        
        resis_A = get_resistance(magnet_A)
        resis_B = get_resistance(magnet_B)
       
        magnet_A.apply_force(force_on_A + gravity_A + resis_A)
        magnet_B.apply_force(force_on_B + gravity_B + resis_B)
        
        A_x, A_y, A_z = magnet_A.position
        B_x, B_y, B_z = magnet_B.position
        
        
        writer.writerow([t, A_x, A_y, A_z, B_x, B_y, B_z])
        
        
        magnet_A.update(dt)
        magnet_B.update(dt)

        
        if step % 10 == 0:
            print(f"Step {step:3d} | 时间: {t:.2f}s | A位置: [{B_x:.4f}, {A_x:.4f}, {A_z:.4f}]")

        t += dt