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
        
        self.trajectory = [self.position.copy()]

    def apply_force(self, force_vector):
       
        self.force += np.array(force_vector, dtype=float)

    def clear_force(self):
       
        self.force = np.zeros(3)

    def update(self, dt):
       
        self.acceleration = self.force / self.mass
  
        self.velocity += self.acceleration * dt
       
        self.position += self.velocity * dt
      
        self.trajectory.append(self.position.copy())
        self.clear_force()

    def get_trajectory_array(self):

        return np.array(self.trajectory)