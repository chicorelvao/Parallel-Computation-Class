"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #3 01-11-2022
    Question 5
    ============================================================

    This code is to be run on four cores or threads.

    As seen in question 4, the code with the break statement creates
    the problem of unificient use of threads, since some
    finish earlier than others.

    The objective, now, is to either make the slower threads calculate
    less points or to make the threads calculations as similar
    as possible. The last option was choosen.

    Instead of dividing the y axis in blocks, but in lines, the
    calculations done by each thread are very similiar, meaning
    that they all end at a similar time, for a given x direction.

    In this program, each thread does a line along the x axis
    and jumps 4 step sizes the next line, until a new break statement.

    The result was very good, because all threads took the same
    amount of time and load.
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


sumOut = 0

for i in range(rank, m, 4):
    x = step/2 + step*rank + i*step

    for j in range(m):
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
# For the rank 0 thread
if rank == 0:
    piCalc = sumOut
    for thread in range(1, threads):
        resultThread = comm.recv(source = thread)
        piCalc += resultThread[0]
        
        print('On process', thread, 'result is', resultThread[0])
        print('Tempo decorrido: ', resultThread[1])

    print('On process', rank, 'result is', sumOut)
    print('Tempo decorrido: ', elaspedTime)

    print(4*piCalc/(m - 1)**2)
else:
    comm.send([sumOut, elaspedTime], dest = 0)



