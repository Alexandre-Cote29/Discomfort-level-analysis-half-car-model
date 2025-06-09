from car_data import list_of_car_dicts as list_d



import random

class CarType(object):

    def __init__(self):
        self.c_d = {} 

    def car_type_parameters(self, car_type_input, randomness=True, symmetrical_axles=False):
        """
        Generates specific car parameters based on type, with optional randomness and symmetry.

        Args:
            car_type_input (str): The type of car (e.g., 'pickup', 'sedan').
            randomness (bool): If True, picks a random value from the range.
                               If False, picks the mean (average) of the range.
            symmetrical_axles (bool): If True, forces k_s1=k_s2, k_t1=k_t2, c1=c2, and m_u_front=m_u_rear.
                                      If False, k_s/k_t/c/m_u are independently picked/averaged from their ranges.
        Returns:
            dict: A dictionary containing the specific (single) parameter values for the car type.
        """
        car_params_definitions = {
            "pickup": {
                "k_s_range": (100000.0, 150000.0),
                "k_t_range": (200000.0, 250000.0),
                "c_range": (5000.0, 8000.0),
                "cg_ratio_range": (0.45, 0.55),
                "m_u_range": (40.0, 60.0),         
                "I_range": (2500.0, 3500.0)
            },
            "sedan": {
                "k_s_range": (80000.0, 120000.0),
                "k_t_range": (180000.0, 220000.0),
                "c_range": (4000.0, 7000.0),
                "cg_ratio_range": (0.48, 0.52),
                "m_u_range": (30.0, 45.0),         
                
            },
            "hatchback": {
                "k_s_range": (70000.0, 110000.0),
                "k_t_range": (170000.0, 210000.0),
                "c_range": (3500.0, 6500.0),
                "cg_ratio_range": (0.49, 0.53),
                "m_u_range": (25.0, 40.0),         
                
            },
            "suv": {
                "k_s_range": (120000.0, 180000.0),
                "k_t_range": (220000.0, 280000.0),
                "c_range": (6000.0, 9000.0),
                "cg_ratio_range": (0.42, 0.50),
                "m_u_range": (50.0, 70.0),         
                
            },
            "minivan": {
                "k_s_range": (110000.0, 160000.0),
                "k_t_range": (200000.0, 260000.0),
                "c_range": (5500.0, 8500.0),
                "cg_ratio_range": (0.46, 0.54),
                "m_u_range": (45.0, 65.0),         
                
            }
        }

        car_type_key = car_type_input.lower()

        if car_type_key not in car_params_definitions:
            print(f'Error: Unknown Car Type "{car_type_input}".')
            raise ValueError(f"Unknown car type: {car_type_input}")
        else:
            raw_params = car_params_definitions[car_type_key]
            processed_params = {}

           
            def _get_value_from_range(value_range, use_randomness):
                min_val, max_val = value_range
                if use_randomness:
                    return random.uniform(min_val, max_val)
                else:
                    return (min_val + max_val) / 2

            
            k_s_val_front = _get_value_from_range(raw_params['k_s_range'], randomness)
            processed_params['k_s1'] = k_s_val_front
            processed_params['k_s2'] = k_s_val_front if symmetrical_axles else _get_value_from_range(raw_params['k_s_range'], randomness)

            
            k_t_val_front = _get_value_from_range(raw_params['k_t_range'], randomness)
            processed_params['k_t1'] = k_t_val_front
            processed_params['k_t2'] = k_t_val_front if symmetrical_axles else _get_value_from_range(raw_params['k_t_range'], randomness)

            
            c_val_front = _get_value_from_range(raw_params['c_range'], randomness)
            processed_params['c1'] = c_val_front
            processed_params['c2'] = c_val_front if symmetrical_axles else _get_value_from_range(raw_params['c_range'], randomness)

            
            m_u_val_front = _get_value_from_range(raw_params['m_u_range'], randomness) 
            processed_params['m_u1']= m_u_val_front
            processed_params['m_u2']= m_u_val_front if symmetrical_axles else _get_value_from_range(raw_params['m_u_range'], randomness)

            
            processed_params['cg_ratio'] = _get_value_from_range(raw_params['cg_ratio_range'], randomness)



            
            self.c_d = processed_params

            print (self.c_d)
            return self.c_d