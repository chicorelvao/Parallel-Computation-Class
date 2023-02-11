"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #6 20-11-2022
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

n = int(sys.argv[1])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
threads =  MPI.COMM_WORLD.Get_size()

# Each thread gets some lines of matrix A
threadLines = n//threads

if rank == 0:

    A = np.random.randint(100, size=(n, n))
    B = np.random.randint(100, size=(n, n))
    # For some reason, the mpi protocol doesn't like int64 np arrays
    A = np.float64(A)
    B = np.float64(B)

    print("Non-threaded Calculation: ")
    C = np.matmul(A, B)
    print(C)
    print("============================")

    # Since I'm using scatter, the A matrix has to be reshaped, so that
    # Each thread gets an array, from the scatter method. 
    # So, the new matrix A has to have has many lines(arrays) as there are threads
    outA = A.reshape((threads, n*threadLines))
    
    # This the ouput array for the Gather method. It's necessary to have it 
    # on the main process, so the gather method works
    resultC = np.zeros((n, n))

else:
    # Using this initializations, it avoids having everything inside the if statement
    outA = None
    B = np.zeros((n,n))
    resultC = None


subA = np.zeros((1, n*threadLines))

comm.Scatter(outA, subA, root=0)
comm.Bcast(B, root=0)


# For a certain thread, A comes in as a linear sub matrix. Naturally
# it needs to be reshaped get the correct sub matrix output.
subA = subA.reshape((threadLines, n))
subC = np.matmul(subA, B)


comm.Gather(subC, resultC, root = 0)

if rank == 0:
    print("Threaded Result: \n", resultC)


