import matplotlib.pyplot as plt
import csv

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  
plt.rcParams['axes.unicode_minus'] = False 


times = []
A_x_list = []
B_x_list = []


with open('simulation_results.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  
    
    for row in reader:
        if len(row) >= 7: 
            times.append(float(row[0]))     
            A_x_list.append(float(row[1]))  
            B_x_list.append(float(row[4]))  


plt.figure(figsize=(30, 6)) 


#plt.plot(times, A_x_list, label='实体 A (A_x)', color='#1f77b4', linewidth=2)


plt.plot(times, B_x_list, color='#ff7f0e', linewidth=2)


plt.title('', fontsize=16)
plt.xlabel('时间 t (s)', fontsize=12)
plt.ylabel('X轴位置 (m)', fontsize=12)

plt.grid(True, linestyle='--', alpha=0.7) 
plt.legend(fontsize=12)                   


plt.show()