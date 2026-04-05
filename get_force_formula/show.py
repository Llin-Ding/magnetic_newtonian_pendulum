import matplotlib.pyplot as plt
import csv


plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  
plt.rcParams['axes.unicode_minus'] = False 

file_path = 'magnetic_force_results.csv' 

distances = [] 
forces = []    

try:
    with open(file_path, 'r', encoding='utf-8') as file:
   
        reader = csv.reader(file)
        
        for row in reader:
            if not row:
                continue 
            
            if len(row) >= 2:
                try:
          
                    distances.append(float(row[0])) 
                    forces.append(float(row[1]))    
                except ValueError:
                   
                    continue


    plt.figure(figsize=(8, 6)) 
    
    plt.plot(distances, forces, color='#1f77b4', linewidth=2, marker='.', label='力-距离曲线')
    
    
    plt.title('力 - 距离关系曲线图', fontsize=16) 
    plt.xlabel('距离 (mm)', fontsize=12)         
    plt.ylabel('力 (N)', fontsize=12)          
    
    plt.grid(True, linestyle='--', alpha=0.7)    
    plt.legend(fontsize=12)                     
    
    plt.show()

except FileNotFoundError:
    print(f"找不到文件：'{file_path}'，请检查文件是否放在了正确的文件夹中！")