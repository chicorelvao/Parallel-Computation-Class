"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #3 01-11-2022
    Question 2
    ============================================================

    This code is to be run on four cores or threads.
"""

from mpi4py import MPI
import numpy as np
import sys
"""
    Chapter 1 - Main Procedure
    ------------------------------------------------------------
"""

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
threads =  MPI.COMM_WORLD.Get_size()


inputN = int(sys.argv[1])
exp = int(sys.argv[2])

# Total number of points
n = inputN**exp

# Side points of the square
m = int(np.sqrt(n))

# Divison of the y axis
mThreads = m//threads

# The inverval goes from -1 and 1
interval = 1
# The distance between the points
deltaM = (2*interval)/(m - 1)

"""
    The grid choice is so that the points are centered 
    in the squares of dicretization. This makes it easier
    to the divide the work by the threads and not repeat
    points. Its just a personal choice. So instead of 
    starting in -1, the code starts at -0.8 or -0.9, etc
    it depends on the step size (deltaM)
"""
limits = (mThreads*rank, mThreads*(rank + 1))

sumOut = 0
for i in range(m):
    x = -interval + deltaM/2 + i*deltaM
    for j in range(limits[0], limits[1]):
        y = -interval + deltaM/2 + j*deltaM
        r = x**2 + y**2

        if r <= 1:
            sumOut += 1



"""
    Chapter 2 - MPI & Results
    ------------------------------------------------------------
"""

if rank == 0:
    resultThread = sumOut
    for thread in range(1, threads):
        
        resultThread += comm.recv(source = thread)
        print('On process', thread, 'result is', resultThread)
        
    
    print(resultThread)

    print("Calculated Value of Pi: ", 4*resultThread/(m - 1)**2)
else:
    
    comm.send(sumOut, dest = 0)


"""
    Recorded Elapsed Time: 19.1 seg.
"""
