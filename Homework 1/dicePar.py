"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #1 21-09-2022
    ============================================================

    This code is to be run on four cores or threads.
"""

from random import randint
import matplotlib.pyplot as plt
from mpi4py import MPI

"""
    Chapter 1 - Main Procedure
    ------------------------------------------------------------
"""
# This code is necessarity to run the livrary
# Init MPI ENV
comm = MPI.COMM_WORLD
# Each thread gets its rank
rank = comm.Get_rank()
# Total number of threads
threads =  MPI.COMM_WORLD.Get_size()

# Each thread will throw two dices n times
n = int(1e7)//threads

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

"""
    Chapter 2 - MPI & Plot
    ------------------------------------------------------------
"""
print(rank)
# For the rank 0 thread
if rank == 0:

    print ('Number of processes:', threads)
    # Print the result on thread 0
    print('On process', rank, 'result is', D)

    # And for each thread
    for thread in range(1, threads):
        # Read the corresponding dictionary
        Dp = comm.recv(source = thread)
        print('On process', thread, 'result is', Dp, sum(Dp[k] for k in Dp))
        # Add the dictionary from each thread, to the general dictionary
        for i in range(2, 13):
            D[i] += Dp[i]
            
    print ('Final result:         ', D, sum(D[k] for k in D))

    # Transform the dict to two arrays, it's easier to plot
    faces = list(D.keys())
    freq = list(D.values())

    print(f"Número Total de Lançamentos (Check): {sum(freq)}")

    # The freq array is normalized, I think it's better present information
    # relative terms.
    freq = [float(i)/sum(freq) for i in freq]

    plt.bar(range(len(faces)), freq, tick_label=faces)
    plt.ylabel('Frequências')
    plt.xlabel('Soma da Faces')
    plt.title('Frequências de Lançamentos')
    plt.show()


else:
    # Each thread sends its dictionary to rank zero thread
    comm.send(D, dest=0)


"""
    Chapter 3 - The Veredict
    ------------------------------------------------------------
    This simulation was run with the mpi API. I measured the run
    time three times:
        - 7s46
        - 7s99
        - 7s74

    Mean Time: 7s73

    Net Gain: -4s16

    The result is rather unexpected, since the use of 3 more cores
    did not cut the elapsed by 75%, but by only 33%, which is still
    usefull, even more for bigger simulations. This could be due to 
    the implementation being efficient.
    
"""