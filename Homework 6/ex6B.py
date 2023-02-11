"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #6 20-11-2022
    ============================================================

    This code is to be run on four cores or threads.
"""

from mpi4py import MPI
import math
import numpy as np
import sys
"""
    Chapter 0 - Functions
    ------------------------------------------------------------
"""

# Each process has to initialize an array to receive 
# the linear sub matrix from the main process.
def subMatrix(scatterArr):
    subArr = np.zeros((1, n*threadLines))
    comm.Scatter(scatterArr, subArr, root=0)

    return subArr

"""
    Chapter 1 - Main Procedure
    ------------------------------------------------------------
"""
n = int(sys.argv[1])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
threads =  MPI.COMM_WORLD.Get_size()

# The algorithm requires that matrix be divided in m segments
m = int(math.sqrt(threads))
# Each segment contains a certain number of lines
threadLines = n//m


if rank == 0:
    # ------------- DEBUG ---------------------------
    #A = np.linspace(1, n**2, n**2 ).reshape((n,n))
    #B = np.linspace(10, 10*n**2, n**2 ).reshape((n,n))


    A = np.random.randint(100, size=(n, n))
    B = np.random.randint(100, size=(n, n))
    # Again, for some reason mpi doesnt like int64 types
    A = np.float64(A)
    B = np.float64(B)

    print("Non-threaded Calculation: ")
    C = np.matmul(A, B)
    print(C)
    print("============================")

    
    # This time, both A and B have to be reshaped. Whereas before
    # the number of segments corresponded to the number of threads,
    # this time around the the combination of the submatrixs of A and B
    # are equal to the number of threads.

    # A and B still have to be linearized, because of Scatter
    outA = A.reshape((m, n*threadLines))

    # Since the m segments are not equal to the number of threads,
    # linear matrix A has to be repeated and so does linear matrix B.
    repeatA = (np.ones((len(outA)))*m).tolist()
    scatterA = np.repeat(outA, repeats=repeatA, axis=0)

    # A and B cannot be repeated on the same pattern, thus the submatrixes
    # combination has to be mismached.
    outB = np.transpose(B).reshape((m, n*threadLines))
    scatterB = np.resize(outB, (threads, n*threadLines))
    

    #print("\nA: \n", A, "\noutA: \n", outA, "\nScatterA : \n", scatterA)
    #print("\nB: \n", B, "\noutB: \n", outB, "\nScatterB: \n", scatterB)
    #print("==============================================")

    # Necessary for the Gather comm
    outC = np.zeros((threads, threadLines**2))

else:
    scatterA = None
    scatterB = None
    outC = None



# Initialization of the arrays that receive the 
# information from the main process
subA = subMatrix(scatterA)
subB = subMatrix(scatterB)

# To perform the correct calculation, the linear submatrixes have to 
# be reshaped
subA = subA.reshape((threadLines, n))
subB = np.transpose(subB.reshape((threadLines, n)))

subC = np.matmul(subA, subB)

# Linear submatrixes are sent to the main process
comm.Gather(subC, outC, root = 0)


if rank == 0:
    resultC = np.zeros(threads, dtype=object)
    
    # Reshape each liner submatrix of the general array of Gather comm
    # to square submatrixes
    for i in range(threads):
        resultC[i] = outC[i].reshape(threadLines, threadLines)

    # This general array has also to be reshaped to a square matrix
    resultC = resultC.reshape(m, m)

    out = []
    
    # Finally, to present the correct matrix, collapse the general array
    # horinzotally and vertically after.
    for i in range(m):
        out.append(np.hstack(resultC[i]))

    out = np.vstack(np.array(out))
    
        
    print("Threaded Result: \n", out)
    
   


    


