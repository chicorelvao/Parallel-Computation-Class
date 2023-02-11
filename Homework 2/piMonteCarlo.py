"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #1 21-09-2022
    ============================================================

    This code is to be run on a single core or thread.
"""

from random import randint, random
import math
import matplotlib.pyplot as plt
import sys
import time


"""
    Chapter 1 - Main Procedure
    ------------------------------------------------------------
"""

# Start Counting the Time
timeInit = time.time()

# The n is obtained from the terminal 
# N is the number of total random points
n = int(float(sys.argv[1]))
    
print (f'you entered {n}')


# Number of points inside de circle
counter = 0

# Generate two numbers for n times
for i in range(n):
    x = random()
    y = random()

    # Calculate the hypotenuse
    r = math.sqrt(x**2 + y**2)
    # If the Hypotenuse is smaller than one, then the point is inside circle 
    # And the counter var is updated
    if r < 1:
        counter += 1

# Stop the time counter and calculate the duration
timeEnd = time.time()

duration = timeEnd - timeInit

"""
    Chapter 2 - Results
    ------------------------------------------------------------
"""

# The value of pi calculated
result = 4*counter/n

print(f"Value of pi calculated: {result}. Duration of the simulation: {duration} seg.")

# Calculation of the error 
ratio = counter/n

Zc = 1

deltaPi = 4*Zc*math.sqrt(ratio*(1 - ratio)/n)

print(f'Error on the pi calculated: {deltaPi}.')

"""
    Chapter 3 - Verdict
    ------------------------------------------------------------
    This simulation was run without the mpi API. I measured the run
    time three times:
        - 364 seg
        - 330 seg
        - 348 seg

"""

