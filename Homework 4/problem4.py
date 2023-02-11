"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #4 06-11-2022
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

# The while loop needs a to terminate the program when
# the mean deviation is smaller than 10^-3. This function
# calculates the mean deviation from a given dictionary.

halfExpected = [1/36, 1/18, 1/12, 1/9, 5/36, 6/36]
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

while True:
    
    if rank == 0:
        print("n: ", n)
        nThread = int(n/threads)

        for thread in range(1, threads):
                comm.send(nThread, dest = thread)

        if nThread > 0:

            D = throwDices(nThread)
            
            for thread in range(1, threads):

                Dp = comm.recv(source = thread)

                for i in range(2, 13):
                    D[i] += Dp[i]

            print("Results: ", D, "\nTotal Dice Throws: ", sum(D.values()))

            sigma = sigmaCalc(D)
            print("Mean Deviation: ", sigma)

            if sigma < 1e-3:
                n = 0

            n = n*2
            
            print("========================================================\n")

        else:
            break
                

    else:
        nThrows = comm.recv(source = 0)

        if nThrows > 0:
            D = throwDices(nThrows)
            comm.send(D, dest = 0)
        else:
            break

