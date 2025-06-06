import pylab as plt
import numpy as np
from my_road_generator import *
from state_space import HalfCarModel
from filter import *
from scipy.signal import periodogram


L = 100
step= 0.01
v= 22.2

n = np.arange(1, int((L/step)//2)+1)
randomness = 2 * np.pi * np.random.rand(len(n))





my_test = MyRoadGenerator()
my_profile = my_test.generate_road_input(L, step, v, randomness)


u = my_test.u_input
t = my_test.t



state_s = HalfCarModel()
state_fnc = state_s.generate_car_result(u, t)

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



print(f'{filtering.rms_signal:.2f}')
plt.show()


