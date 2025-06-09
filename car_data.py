import pandas as pd
import random
import numpy as np # Used for checking for NaN values

# 1. Read your CSV file with the correct separator and decimal
car_csv = pd.read_csv("car_data.csv", sep=';', decimal=',')

# Function to calculate the random mass for a given row
def calculate_single_mass(row):
    min_mass = row['Minimum Mass (kg)']
    max_mass = row['Maximum Mass (kg)']

    # Handle cases where max_mass is missing or 0
    # pd.isna() checks for NaN values (Not a Number)
    if pd.isna(max_mass) or max_mass == 0:
        effective_max_mass = min_mass + 60
    else:
        effective_max_mass = max_mass

    # Ensure min_mass is not accidentally greater than effective_max_mass
    # (e.g., if min_mass + 60 was less than initial min_mass due to some weird data)
    # This scenario is unlikely with your rule, but it's good practice for random.uniform
    if min_mass > effective_max_mass:
        effective_max_mass = min_mass # Or handle as an error/warning

    # Generate a random float between min_mass and effective_max_mass
    return random.uniform(min_mass, effective_max_mass)

# 2. Apply the function to each row to create a new 'mass' column
#    'axis=1' ensures the function is applied row-wise
car_csv['mass'] = car_csv.apply(calculate_single_mass, axis=1)

# 3. Drop the original 'Minimum Mass (kg)' and 'Maximum Mass (kg)' columns
car_csv = car_csv.drop(columns=['Minimum Mass (kg)'])

# 4. Convert the streamlined DataFrame to a list of dictionaries
list_of_car_dicts = car_csv.to_dict(orient='records')


