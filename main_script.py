import pylab as plt
import numpy as np
from my_road_generator import *
from state_space import HalfCarModel
from car_type import CarType
from filter import *
from scipy.signal import periodogram
from car_data import list_of_car_dicts

L = 200
step= 0.01
v= 22.2

#Road roughness: How do we input it into the model!!!


my_test = MyRoadGenerator()
my_profile = my_test.generate_road_input(L, step, v)

w = list_of_car_dicts[0]
u = my_test.u_input
t = my_test.t

car_params_generator = CarType()
car_specific_params = car_params_generator.car_type_parameters(
    w['Car Type'],
    randomness=True,
    symmetrical_axles=True
)


m_s = w['mass']
wb = w['Wheelbase (mm)']
k_s1 = car_specific_params['k_s1']
k_s2 = car_specific_params['k_s2']
c1 = car_specific_params['c1']
c2 = car_specific_params['c2']
k_t1 = car_specific_params['k_t1']
k_t2 = car_specific_params['k_t2']
m_u1 = car_specific_params['m_u1']
m_u2 = car_specific_params['m_u2']
cg_ratio = car_specific_params['cg_ratio']
a = wb * cg_ratio
b = wb * (1 - cg_ratio)

#Inertia approximation
if w['Car Type'] == 'Pickup':
    I = 3.182*m_s -2107.468
else:
    I = 3.079*m_s - 1728.758


state_s = HalfCarModel(
   mass=m_s,      
    k_s1=k_s1,     
    k_s2=k_s2,     
    c1=c1,         
    c2=c2,         
    k_t1=k_t1,     
    k_t2=k_t2,     
    m_u1=m_u1,     
    m_u2=m_u2,     
    a=a,           
    b=b,
    I = I            
)
state_fnc = state_s.generate_car_result(t, u)

filtering = Filtering()
filt = filtering.ISO_2631_filter(state_s.y, 1/my_test.dt)



# Plotting

plt.figure()

plt.subplot(2,2,1)
plt.title('Periodogram')
plt.loglog(*periodogram(state_s.y,fs=1/my_test.dt), 'green', label='Acceleration (unfiltered)')
plt.loglog(*periodogram(my_test.u_front,fs=1/my_test.dt), 'red', label='Road Profile')
plt.loglog(*periodogram(filtering.filtered_signal, fs=1/my_test.dt), 'blue', label = 'Acceleration (filtered)')
plt.xlabel("Frequency")
plt.ylabel("PSD")
plt.ylim(1e-12, 1000)
plt.grid("on")
plt.legend()



plt.subplot(2,2,2)
plt.title('Acceleration through the road')
plt.plot(state_s.t_out, filtering.filtered_signal, label = "Filtered", zorder=2 )
plt.plot(state_s.t_out, state_s.y, label = 'Unfiltered', zorder = 1)
plt.xlabel('Time(s)')
plt.ylabel('Acceleration(m/s^2)')
plt.grid('on')
plt.legend()



plt.subplot(2, 2, 3)
plt.title('Road Profile')
plt.plot(my_test.t, my_test.u_front, 'blue', label= 'Front Wheel')
plt.plot(my_test.t, my_test.u_rear, 'green', label = 'Rear wheel')
plt.legend()
plt.grid('on')




plt.show()

print(f'{filtering.rms_signal:.2f}')
