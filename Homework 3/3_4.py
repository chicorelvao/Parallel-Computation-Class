"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #3 01-11-2022
    Question 4
    ============================================================

    This code is to be run on four cores or threads.
"""
from mpi4py import MPI
import numpy as np
import sys
import time
"""
    Chapter 1 - Main Procedure
    ------------------------------------------------------------
"""

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
threads =  MPI.COMM_WORLD.Get_size()

inputN = int(sys.argv[1])
exp = int(sys.argv[2])

timeInit = time.time()

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
        else:
            break

timeEnd = time.time()
elaspedTime = timeEnd - timeInit
"""
    Chapter 2 - MPI & Results
    ------------------------------------------------------------
"""

if rank == 0:
    piCalc = sumOut
    totalTime = elaspedTime

    for thread in range(1, threads):
        resultThread = comm.recv(source = thread)
        piCalc += resultThread[0]
        totalTime += resultThread[1]
        
        print('On process', thread, 'result is', resultThread[0])
        print('Tempo decorrido: ', resultThread[1])


    print('On process', rank, 'result is', sumOut)
    print('Tempo decorrido: ', elaspedTime)

    piCalc = 4*piCalc/(m - 1)**2
    print("Pi: ", piCalc)
    
else:
    comm.send([sumOut, elaspedTime], dest = 0)


"""
    Elapsed Time: 14 seg

    Naturlly, the elapsed time descreased, but the precision
    remains the same, because there were not fundamental changes
    in the way the pi value is calculated, the code is almost
    the same as for question 3.
"""


