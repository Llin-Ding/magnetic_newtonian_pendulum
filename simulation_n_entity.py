from physical_entity import Entity
import numpy as np
import csv
from get_force import get_ac_gravity, get_force_at_distance, get_resistance

# === 仿真基础参数 ===
n = 5  # 设置摆的数量
t = 0
dt = 0.05 
steps = 10000
mass = 0.0022  # 质量 2.2g

# === 初始化 N 个摆 ===
magnets = []
spacing = 0.059  # 假设每个摆的悬挂点(平衡点)间隔 0.059m

for i in range(n):
    # 计算每个摆的悬挂点(平衡点)
    balance_point = np.array([i * spacing, 0, 0])
    
    # 设置初始位置：这里演示让第 2 个摆（索引为 1）有一个初始偏移，其他在平衡位置
    if i == 1:
        start_pos = [0.080, 0, 0]
    else:
        start_pos = [i * spacing, 0, 0]
        
    start_vel = [0, 0, 0]
    
    # 实例化实体
    magnet = Entity(mass=mass, initial_position=start_pos, initial_velocity=start_vel)
    magnet.init_pos = balance_point  # 供重力/回复力函数使用
    
    magnets.append(magnet)


# === 运行仿真并写入 CSV ===
with open(f'simulation_results_{n}.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
 
    # 动态生成表头: ['Time_s', 'M0_x', 'M0_y', 'M0_z', 'M1_x', ...]
    header = ['Time_s']
    for i in range(n):
        header.extend([f'M{i}_x', f'M{i}_y', f'M{i}_z'])
    writer.writerow(header)
    
    # 开始时间步循环
    for step in range(steps):
        
        # 1. 初始化每个摆在当前步的受力总和容器
        # （如果你的 Entity.apply_force 会自动累加力，这里需要在类内清零；
        #   通常物理引擎每一帧会重新计算合力，所以我们在外部用一个列表暂存）
        total_forces = [np.zeros(3) for _ in range(n)]
        
        # 2. 计算两两之间的相互作用力 (O(N^2) 复杂度)
        for i in range(n):
            for j in range(i + 1, n):  # 从 i+1 开始，避免重复计算和计算自身
                # get_force_at_distance(目标, 源) -> 计算 j 受到来自 i 的力
                force_on_j_from_i = get_force_at_distance(magnets[j], magnets[i])
                
                total_forces[j] += force_on_j_from_i
                total_forces[i] -= force_on_j_from_i  # 牛顿第三定律：反作用力
                
        # 3. 计算独立受力（重力回复力、阻力）并施加总力
        for i in range(n):
            gravity_i = get_ac_gravity(magnets[i])
            resis_i = get_resistance(magnets[i])
            
            # 合力 = 相互作用力 + 重力回复力 + 阻力
            magnets[i].apply_force(total_forces[i] + gravity_i + resis_i)
        
        # 4. 记录数据到 CSV
        row_data = [t]
        for magnet in magnets:
            row_data.extend(magnet.position)
        writer.writerow(row_data)
        
        # 5. 更新所有摆的运动状态
        for magnet in magnets:
            magnet.update(dt)

        # 6. 控制台打印进度 (这里只打印第一个和第二个摆的 x 坐标作为参考)
        if step % 10 == 0:
            print(f"Step {step:4d} | 时间: {t:.2f}s | 摆0位置X: {magnets[0].position[0]:.4f} | 摆1位置X: {magnets[1].position[0]:.4f}")

        t += dt