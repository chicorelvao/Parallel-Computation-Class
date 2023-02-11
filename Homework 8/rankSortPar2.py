"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #8 06-12-2022
    ============================================================

    This code is to be run on four cores or threads.
"""



import numpy as np
from sys import argv
from mpi4py import MPI
import datetime


"""
    Chapter 0 - Initializions and Allocations
    ------------------------------------------------------------
"""
# The seed method allows for the use of random related numbers.
# It's a very interesting topic.
#np.random.seed(13)
n = int(argv[1])
debug = argv[1][0] == '+'


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
threads =  MPI.COMM_WORLD.Get_size()


"""
    Chapter 1 - Functions
    ------------------------------------------------------------
"""

# Debug

def ts_print (message):
    now = datetime.datetime.now()
    timestamp = now.strftime('%H:%M:%S.%f')
    print (f'Rank: {rank}, [{timestamp}] {message}', flush=True)

def debug_print (message):
    if debug:
        ts_print (message)


# Sorting Functions

# This functions compares the full unsorted array with the elements
# of the unsorted smaller arrays assigned to each thread.
# The sub arrays are assigned by the master using slices, or index intervals 
# of the array to be sorted. It's this slices that are sent to the
# corresponding thread. 
# No smaller subarrays of the unsorted array are sent to the threads.

def getRankSort(unSortedArr, indexes):

    # This is the scarescrow subarray, thus avoiding reciving two arrays
    # from the master thread
    threadUnsortedArr = unSortedArr[slice(indexes[0], indexes[1])]

    nUnsorted = len(threadUnsortedArr) 

    # Mask to be given to the master thread
    r = np.empty(nUnsorted, dtype=int)

    for i in range(nUnsorted):
        x = 0
        for j in range(n):
            if threadUnsortedArr[i] > unSortedArr[j]:
                x += 1
        r[i] = x

    return r


# Communication Functions

# Since this is a parallel program, the  full unsorted array has to be 
# broken up by smaller arrays, while avoiding to send each subarray. 
# This algorithm provides a fair share of the full array between the threads.
# E.g.: len(unsorted) = 10
#       [3, 3, 2, 2] -> Fair
#       [4, 3, 2, 1] -> Not Fair
#
# The output of this function is an array with the per thread lengths of
# the unsorted array. 

def subArraysLen(numbersLen):
    x = np.zeros((int(threads)), dtype=int)

    for i in range(threads):
        x[i] += int(numbersLen//threads)

    leftOver = numbersLen%threads
    
    for i in range(leftOver):
        x[i] += 1

    return x


# This functions is runned by the master thread, to produce arrays 
# to be sent to the threads with the slices, following a fair share of 
# the full unsorted array size between the threads. 
# In this case, an index interval only requires to numbers.
# Remmenber, the unsorted array is never sent twice.

def scatterArray(nThreadsArr):
    
    auxList = np.empty((1,2), dtype=int)

    # Indexes of the full array are used to break it up
    indexCounter = 0 

    for nThread in nThreadsArr:
        threadIndexes = np.zeros(2, dtype=int)

        indexLastElement = indexCounter + nThread

        threadIndexes[0] = indexCounter
        threadIndexes[1] = indexLastElement

        auxList = np.vstack((auxList, threadIndexes))

        indexCounter = indexLastElement

    return auxList[1:]
    

"""
    Chapter 3 - Main Procedure
    ------------------------------------------------------------
"""

if rank == 0:
    # The array to be sorted
    a = np.random.rand(n)
    nThreads = subArraysLen(n)
    toSendArray = scatterArray(nThreads)


    debug_print(f"Array to be Sorted: {a}")
    debug_print(f"Lengths For Each Thread: {nThreads}")
    debug_print(f"Index Array Scatter by Master: {toSendArray}")

    

else:
    toSendArray = None
    a = np.empty(n)



threadIndexes = np.empty(2, dtype=int)

comm.Bcast(a, root=0)
comm.Scatter(toSendArray, threadIndexes, root=0)

threadSortedMask = getRankSort(a, threadIndexes)

debug_print(f"Casted Full Unsorted Array: {a}")
debug_print(f"Thread Index Interval Received: {threadIndexes}")
debug_print(f"Rank Sorted Array Masks: {threadSortedMask}")


if rank != 0:
    comm.Send([threadSortedMask, MPI.INT], dest=0)


else:
    # Merge the sub masks from each thread
    maskArray = threadSortedMask.copy()

    # Numpy doesn't like arrays with subarrays of diferent size,
    # So I have to use Recv/Send or gather (pickle)
    for i in range(1, threads):
        auxArr = np.empty(nThreads[i], dtype=int)
        comm.Recv(auxArr, source=i)
        maskArray = np.hstack((maskArray, auxArr))

    debug_print(f"Merged Array Mask: {maskArray}")



    # Sort the initial array with the mask
    b = np.empty(n, dtype=float)

    for i in range(n):
        b[maskArray[i]] = a[i]



    # Check if it's sorted
    isSorted = lambda x: (np.diff(x)>=0).all()
    check = isSorted(b)



    print("\n\n\n==================== Results ====================\n")
    print ('Initial Unsorted Array: ' + ', '.join(("%5.3f" % x) for x in a))
    print ('Rank Sort Mask: ' + ', '.join(("%5d" % x) for x in maskArray))
    print ('Sorted Array: ' + ', '.join(("%5.3f" % x) for x in b))

    print(f"Ascending Order Check: {check}")

