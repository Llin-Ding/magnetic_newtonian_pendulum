import numpy as np
from get_magnet import get_hollow_cylinder
import time
from tqdm import tqdm



def get_force(source_magnet, location, B_z, h, r_in, r_out, delta_m = 0.0001):
    
    _, valid_positions, magt = get_hollow_cylinder(r_in, r_out, h, B_z, location=location)
    

    pos_x_plus = valid_positions + np.array([delta_m, 0, 0])
    pos_x_minus = valid_positions - np.array([delta_m, 0, 0])


    Bz_plus_T = source_magnet.getB(pos_x_plus)[:, 2]
    Bz_minus_T = source_magnet.getB(pos_x_minus)[:, 2]


    dBz_dx = (Bz_plus_T - Bz_minus_T) / (2 * delta_m)


    force_x_elements = magt * dBz_dx
    F_x_total = np.sum(force_x_elements)

    return F_x_total


def generate_force_csv(start_m, end_m, step_m, filename="magnetic_force.csv", 
                       B_z=1.0, h=0.0073, r_in=0.0018, r_out=0.00385):
    
    print(f"开始生成磁力文件 -> {filename}")
    print(f"扫描范围: {start_m*1000:.1f} mm 到 {end_m*1000:.1f} mm (步长 {step_m*1000:.2f} mm)")
    
    start_time = time.time()
    
    source_magnet = get_hollow_cylinder(r_in, r_out, h, B_z, location=(0, 0, 0), grid=False)
    
    distances_m = np.arange(start_m, end_m + step_m/2, step_m)
    results = []
 
    for i, dist in enumerate(tqdm(distances_m, desc="计算进度", colour='green')):
        force = get_force(source_magnet, (dist, 0, 0), B_z, h, r_in, r_out)
        results.append([dist, force])
        
    results_array = np.array(results)
    np.savetxt(
        filename, 
        results_array, 
        delimiter=",", 
        header="Distance_m,Force_N", 
        comments="",
        fmt="%.8f"
    )
    
    elapsed = time.time() - start_time
    print(f"完成！耗时 {elapsed:.2f} 秒。文件已保存至: {filename}\n")