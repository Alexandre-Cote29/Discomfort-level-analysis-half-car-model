import numpy as np



class MyRoadGenerator(object):

    def __init__(self, S0=(32e-6)/(2*np.pi), Omega0= 2*np.pi): # Omega0 be careful of units: rad/m not 1/m

        
        self.S0 = S0
        self.Omega0 = Omega0
        self.t = None
        self.u_front = None
        self.u_rear = None
        self.u_input = None
        self.z = None
        self.x_road = None

    def generate_road_input(self, L=100, dx=0.01, v=100, seed=None, wb = 2.500):
        """
        Generate road displacement input u(t) for a moving vehicle.

        Args:
            L: Total road length (m)
            v: Vehicle speed (m/s)
            dt: Time step (s)
            S0: Spectral density base value (rad/m^3)
            Omega0: Reference spatial frequency (rad/m)

        Returns:
            t: time vector (s)
            u: road displacement u(t)
        """
        N = int(L/dx)
        self.x_road = np.linspace(0, L, N)
        t_delay = wb/v
    
        
        
        # Frequencies
        
        omega_max = 4*np.pi*2
        omega_min = 0.0078*2*np.pi
        self.Omega_n = np.linspace(omega_min, omega_max, num=N//2 )
        #dOmega = self.Omega_n[1] - self.Omega_n[0]
        dOmega = (omega_max-omega_min)/(N//2)
        S_Omega = self.S0 * (self.Omega_n / self.Omega0)**(-2)
        phi = seed
    
        

        # Generate z(x)
        self.z = np.zeros_like(self.x_road)
        amplitudes = np.sqrt(2 * S_Omega * dOmega)
        for i, xi in enumerate(self.x_road):
            self.z[i] = np.sum(amplitudes * np.cos(self.Omega_n * xi + phi))

        # Convert to u(t)
        self.dt = dx/v
        self.t = np.round(np.arange(0, L / v, self.dt), 100)
       # if self.t[0]< 0:
            #self.t[0] = 0.0
        x_t = v * self.t
        self.u_front = np.interp(x_t, self.x_road, self.z)  # interpolate z(x) at x(t)
        t_rear = self.t - t_delay
        self.u_rear = np.interp(t_rear, self.t, self.u_front, left=self.u_front[0], right=self.u_front[-1])
        self.u_input = np.column_stack([self.u_front, self.u_rear])
    

    
        

        
        return self.t, self.u_front, self.z, self.dt, self.x_road, self.u_rear, self.u_input



if __name__ == '__main__':
    # Create a RoadProfile instance
    testprofile = MyRoadGenerator()
    hihi = testprofile.generate_road_input()
    print(hihi)
    

    
    
    
 



