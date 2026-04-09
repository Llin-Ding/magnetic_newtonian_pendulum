import numpy as np

class Entity:
    def __init__(self, mass, initial_position=(0,0,0), initial_velocity=(0,0,0)):
        if mass <= 0:
            raise ValueError("实体的质量必须大于0")
            
        self.mass = float(mass)
        self.init_pos = initial_position
        self.position = np.array(initial_position, dtype=float)
        self.velocity = np.array(initial_velocity, dtype=float)

        self.force = np.zeros(3)
        self.acceleration = np.zeros(3)
        
        # --- 核心新增：用于缓存错位的半步速度 ---
        self._half_vel = None
        
        self.trajectory = [self.position.copy()]

    def apply_force(self, force_vector):
        self.force += np.array(force_vector, dtype=float)

    def clear_force(self):
        self.force = np.zeros(3)

    def update(self, dt):
        """
        利用半步缓存技巧，在单次调用中实现与 Velocity Verlet 等价的辛积分。
        """
        self.acceleration = self.force / self.mass
        
        # 1. 闭环：利用当前新位置受到的力，完成【上一个时间步】速度的后半步更新
        # （第一步时 _half_vel 为空，跳过此步）
        if self._half_vel is not None:
            self.velocity = self._half_vel + 0.5 * self.acceleration * dt
            
        # 2. 准备：计算【当前时间步】的半步速度
        # v(t + dt/2) = v(t) + 0.5 * a(t) * dt
        self._half_vel = self.velocity + 0.5 * self.acceleration * dt
        
        # 3. 推进：利用半步速度更新位置
        # r(t + dt) = r(t) + v(t + dt/2) * dt 
        # (这在数学上完全等价于 Verlet 位置公式: r + v*dt + 0.5*a*dt^2)
        self.position += self._half_vel * dt
        
        # 记录轨迹并清理力场
        self.trajectory.append(self.position.copy())
        self.clear_force()

    def get_trajectory_array(self):
        return np.array(self.trajectory)