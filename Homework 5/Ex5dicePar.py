"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #5 15-11-2022
    ============================================================

    This code is to be run on four cores or threads.
"""

from random import randint
from mpi4py import MPI
import math
"""
    Chapter 0 - Functions
    ------------------------------------------------------------
"""

# The while loop needs a value to terminate the program when
# the mean deviation is smaller than 10^-3. This function
# calculates the mean deviation from a given dictionary.

halfExpected = [1/36, 1/18, 1/12, 1/9, 5/36, 6/36]
# There are the expected face frequencies from two dice throws
expected = halfExpected + list(reversed(halfExpected[0:5]))

def sigmaCalc(Dict):

    sumDict = 0

    dictIndex = 2

    for expFreq in expected:
        faceFreq = Dict[dictIndex]/sum(Dict.values())
        sumDict = ((faceFreq - expFreq)/expFreq)**2

        dictIndex += 1

    deviation = (1/11)*math.sqrt(sumDict)

    return deviation
        
# This is the main part of the dice throws simulation
def throwDices(n):
    D = {}

    for i in range(2, 13):
        D[i] = 0
        
    for i in range(n):
        # Throw two dices
        v = randint(1, 6)
        g = randint(1, 6)
        # Sum their faces
        sumFaces = v + g
        D[sumFaces] += 1
    
    return D


"""
    Chapter 1 - Main Procedure
    ------------------------------------------------------------
"""

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
threads =  MPI.COMM_WORLD.Get_size()

n = 1024

if rank == 0:

    while True:
        print("New Simulation.\nTotal Throws: ", n)

        nThread = int(n/threads)
        # The master process send the number of throws, before doing its own simulation
        # This is very important to avoid inefficient use of the threads
        nThrows = comm.bcast(nThread, root=0)

        if nThread > 0:
            print(f"Rank: 0 Throws: {nThrows}", flush=True)
            D = throwDices(nThread)
        else:
            print("Simulation Ended. :)")
            break

        threadArr = comm.gather(D, root = 0)

        # D is the result of the master thread. threadArr also contains D (inner workings of mpi)
        # One must be carefull to not repeat the sum of D, when summing the other thread results to D
        for dictionary in threadArr[1:]:
            for i in range(2, 13):
                D[i] += dictionary[i]

        print("Results: ", D, "\nTotal Dice Throws: ", sum(D.values()))

        sigma = sigmaCalc(D)
        print("Mean Deviation: ", sigma)
        print("========================================================\n")

        if sigma < 1e-3:
            n = 0

        n = n*2
            

else: 
    while True:
        # Initialization of the nThread value, even though its not very pythonic.
        # The bcast method from the comm class, requieres a variable in its arguments.
        # Whitout it, it breaks the program.
        nThread = 0
        nThrows = comm.bcast(nThread, root=0)
        

        # this if statement is what ends the simulation. The master will send a zero throws simulations, to stop the
        # thread and get out ot the loop.
        if nThrows > 0:
            print(f"Rank: {rank} Throws: {nThrows}", flush=True)
            Dthread = throwDices(nThrows)
            Dthread = comm.gather(Dthread, root = 0)
        else:
            break


