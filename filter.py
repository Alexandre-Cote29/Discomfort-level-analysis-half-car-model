import numpy as np
from scipy.signal import bilinear, lfilter

class Filtering:

    def __init__(self):
        
        self.rms_signal = None
        self.filtered_signal = None

    def ISO_2631_filter (self, a_signal, fs):


        num_s = [87.72, 1138, 11336, 5453, 5509]
        den_s = [1, 92.6854, 2549.83, 25969, 81057, 79783]

        b_digital, a_digital = bilinear(num_s, den_s, fs)

        self.filtered_signal = lfilter(b_digital, a_digital, a_signal)

        self.rms_signal = np.sqrt(np.mean(self.filtered_signal**2))
        


        return self.rms_signal, self.filtered_signal
    


    


