"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #3 01-11-2022
    Question 3
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

n = inputN**exp


m = int(np.sqrt(n))

mThreads = m//threads
interval = 1
step = (interval)/(m - 1)


limits = (mThreads*rank, mThreads*(rank + 1))

sumOut = 0

for i in range(m):
    x = step/2 + i*step

    for j in range(limits[0], limits[1]):
        y = step/2 + j*step
        r = x**2 + y**2

        if r <= 1:
            sumOut += 1

"""
    Chapter 2 - MPI & Results
    ------------------------------------------------------------
"""
# For the rank 0 thread
if rank == 0:
    resultThread = sumOut

    for thread in range(1, threads):
        resultThread += comm.recv(source = thread)
        print('On process', thread, 'result is', resultThread)

    print(4*resultThread/(m - 1)**2)

else:
    comm.send(sumOut, dest = 0)


"""
    The precision, naturally, increases, since the step size between
    grid points is smaller. The calculated value of pi should have a 
    lower error than the full circle calculation, because the density
    of points has increased. (Law of Large Numbers)

    Total Elapsed Time: 17.6 seg.

    Since the number of points is still the same, as for question 2, the
    elapsed time shouldn't really change.
"""
