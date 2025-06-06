import numpy as np
from scipy import signal as sg
from my_road_generator import*
import os




class HalfCarModel(object):

    def __init__(self):
        self.y = None
        self.t_out = None
        self.x_out = None
        self.sys = None

    def generate_car_result(self, u, t):
      

    
    
        m_s = 1112  
        m_u1 = 40
        m_u2 = 40
        k_s1 = 32.5*1000 
        k_s2 = 27.5*1000 
        k_t1 = 150*1000
        k_t2 = 150*1000
        c1 = 2500 #front
        c2 = 2500
        wb = 2.500
        cg = 0.4
        a = wb - wb*cg # front
        b = wb-a  # back
        I = 2750 #kgm^2



        """
        x1 = Front disp
        x2 = Front speed
        x3 = Rear disp
        x4 = Rear speed
        x5 = Sprung disp
        x6 = Sprung speed
        x7 = Angular disp
        x8 = Angular speed
        """

        # State-space matrices
        A = np.array([
        [0, 1, 0, 0, 0, 0, 0, 0,],
        [-(k_s1 + k_t1)/m_u1, -c1/m_u1,0, 0, k_s1/m_u1, c1/m_u1, (k_s1*a)/m_u1, (a*c1)/m_u1],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, -(k_s2 + k_t2)/m_u2, -c2/m_u2, k_s2/m_u2, c2/m_u2, -(b*k_s2)/m_u2, -(b*c2)/m_u2],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [k_s1/m_s, c1/m_s, k_s2/m_s, c2/m_s, -(k_s1+k_s2)/m_s, -(c1+c2)/m_s, (b*k_s2 - a*k_s1)/m_s, (b*c2 - a*c1)/m_s],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [a * k_s1 / I, a * c1 / I, -b * k_s2 / I,  -b * c2 / I, (-a * k_s1 + b * k_s2) / I, (-a * c1 + b * c2) / I, -(a**2 * k_s1 + b**2 * k_s2) / I, -(a**2 * c1 + b**2 * c2) / I ]

        ])

        B = np.array([
            [0, 0],
            [k_t1/m_u1, 0],
            [0, 0],
            [0, k_t2/m_u2],
            [0,0],
            [0,0],
            [0,0],
            [0,0]
        ])

        C = np.array([
            [k_s1/m_s, c1/m_s, k_s2/m_s, c2/m_s, -(k_s1+k_s2)/m_s, -(c1+c2)/m_s, -(k_s2*b - k_s1*a)/m_s, -(c2*b - c1*a)/m_s]
            ])

        D = np.array([
            [0, 0]
            ])



        # Define system
        self.sys = sg.StateSpace(A, B, C, D)

        


        self.t_out, self.y, self.x_out = sg.lsim(self.sys, U=u , T=t)
        
        #t2_out, y2, x2_out = lsim(sys, U= testprofile.profile, T= testprofile.x)
        return self.t_out, self.y, self.x_out
    



    

    


