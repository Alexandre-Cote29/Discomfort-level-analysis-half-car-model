import numpy as np
from scipy import signal as sg




class HalfCarModel(object):

   
    def __init__(self, mass, k_s1, k_s2, c1, c2, k_t1, k_t2, m_u1, m_u2, a, b, I):
        

        self.m_s = mass
        self.k_s1 = k_s1
        self.k_s2 = k_s2
        self.c1 = c1
        self.c2 = c2
        self.k_t1 = k_t1
        self.k_t2 = k_t2
        self.m_u1 = m_u1
        self.m_u2 = m_u2
        self.a = a
        self.b = b
        self.I = I
       
        """
         State Space X Vector:
        
         1. Front axle displacement
         2. Front axle speed
         3. Rear axle displacement
         4. rear axle speed
         5. Sprung mass displacement
         6. Sprung mass speed
         7. Sprung mass angular displacement
         8. Sprung mass angular speed

       """
        self.A = np.array([
            [0, 1, 0, 0, 0, 0, 0, 0],
            [-(self.k_s1 + self.k_t1)/self.m_u1, -self.c1/self.m_u1, 0, 0, self.k_s1/self.m_u1, self.c1/self.m_u1, (self.k_s1*self.a)/self.m_u1, (self.a*self.c1)/self.m_u1],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, -(self.k_s2 + self.k_t2)/self.m_u2, -self.c2/self.m_u2, self.k_s2/self.m_u2, self.c2/self.m_u2, -(self.b*self.k_s2)/self.m_u2, -(self.b*self.c2)/self.m_u2],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [self.k_s1/self.m_s, self.c1/self.m_s, self.k_s2/self.m_s, self.c2/self.m_s, -(self.k_s1+self.k_s2)/self.m_s, -(self.c1+self.c2)/self.m_s, (self.b*self.k_s2 - self.a*self.k_s1)/self.m_s, (self.b*self.c2 - self.a*self.c1)/self.m_s],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [self.a * self.k_s1 / self.I, self.a * self.c1 / self.I, -self.b * self.k_s2 / self.I, -self.b * self.c2 / self.I, (-self.a * self.k_s1 + self.b * self.k_s2) / self.I, (-self.a * self.c1 + self.b * self.c2) / self.I, -(self.a**2 * self.k_s1 + self.b**2 * self.k_s2) / self.I, -(self.a**2 * self.c1 + self.b**2 * self.c2) / self.I ]
        ])

        self.B = np.array([
            [0, 0],
            [self.k_t1/self.m_u1, 0],
            [0, 0],
            [0, self.k_t2/self.m_u2],
            [0,0],
            [0,0],
            [0,0],
            [0,0]
        ])

        
        self.C = np.array([
            [self.k_s1/self.m_s, self.c1/self.m_s, self.k_s2/self.m_s, self.c2/self.m_s,
             -(self.k_s1+self.k_s2)/self.m_s, -(self.c1+self.c2)/self.m_s,
             (self.b*self.k_s2 - self.a*self.k_s1)/self.m_s, (self.b*self.c2 - self.a*self.c1)/self.m_s]
        ])

        self.D = np.array([
            [0, 0]
        ])

        
        self.sys = sg.StateSpace(self.A, self.B, self.C, self.D)

    
    def generate_car_result(self, time_vector, road_input_matrix):
       

       
        if road_input_matrix.ndim == 1: 
            raise ValueError("road_input_matrix must be a 2D array [front_road, rear_road]")
        if road_input_matrix.shape[0] == 2: 
            road_input_matrix = road_input_matrix.T 


        self.t_out, self.y, self.x_out = sg.lsim(self.sys, U=road_input_matrix, T=time_vector)

        return self.t_out, self.y, self.x_out
    



    

    


