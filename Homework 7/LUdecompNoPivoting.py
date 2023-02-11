"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #7 20-11-2022
    ============================================================

    This code is to be run on four cores or threads.
"""

from mpi4py import MPI
import numpy as np
import datetime

"""
    Chapter 0 - Initialization
    ------------------------------------------------------------
"""

debug = False

#np.random.seed(15) Using this avoids the hassle of saving files and upload files

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
threads =  MPI.COMM_WORLD.Get_size()

# Number of equations
n = np.random.randint(16, 40)

# Initializion of A and b by random methods
if rank == 0:
    if not debug:
        print("Debug is offline.")
    else:
        print("Debug is online.")
    
    AInit = np.random.randint(100, size=(n, n))
    bInit = np.random.randint(100, size=(n, 1))

    A = np.float64(AInit)
    b = np.float64(bInit)
    # A and b are stack to make the LU easier
    A = np.hstack([A, b])
    print("[A|b]:\n", A)
    print("==============================\n")

"""
    Chapter 1 - Functions
    ------------------------------------------------------------
"""

# Debug Functions------------------------------------------------------------------
def ts_print (message):
    now = datetime.datetime.now()
    timestamp = now.strftime('%H:%M:%S.%f')
    print (f'Rank: {rank}, [{timestamp}] {message}', flush=True)

def debug_print (message):
    if debug:
        ts_print (message)
        

# Single Thread Functions ----------------------------------------------------------

# This function performs LU decomp between the pivot line and the line in question,
# because the lines will distributed in bulk to the threads. This works like a microservice.
# Easier to debug and manage.
def newLine(m, array, pivot, phase):

    currentLine = array[1]
    upperLine = array[0]

    k = currentLine[phase]/pivot
    newLine = np.zeros(m)
    
    newLine = currentLine - k*upperLine

    return newLine


# The pivoting is done by the master. First, it checks if the current pivot the samller, 
# then #  it finds the maximum value in a column and it changes  the pivot line by 
# a new one with the new maximum pivot.
def pivoting(pivot, phase, A):

    pivotColumn = A[:, phase][phase:]
    minPivot = np.min(pivotColumn)

    if pivot == minPivot:
        newPivotLine = phase + np.argmax(pivotColumn)

        pivotLine = A[phase, :].copy()

        A[phase, :] = A[newPivotLine, :]
        A[newPivotLine, :] = pivotLine

        pivot = np.max(pivotColumn)

    return A, pivot


# In the end, I want to compare my results with numpy and built this backwards solver.
# Maybe it's  not necessary to have it, since I can simply do matmul( upperA, newb). 
# Anyway, if after a LU decomp was performed and some diagonal element is zero,
# this function also prevents errors and stops the comparison with numpy.
def solverLU(A, b):

    xVec = np.zeros(n)
    stopComparison = False

    for line in range(n - 1, -1, -1):
        currentLine = A[line, :]

        if abs(A[line, line]) > 10**(-12):
            xVec[line] = b[line] - np.matmul(currentLine, xVec)
            xVec[line] = xVec[line]/A[line, line]
        else:
            print("Non linear set of equations after LU decomposition was performed.")
            stopComparison = True
            break

    
    return xVec, stopComparison

# Thread Communication -----------------------------------------------------------------------

# To send the lines, or equations to each thread, I need to know how many equations
# are left to have the LU decomp performed on then.
# This is a simple intiger distributor, so that the threads get a fair number of lines.
# For example, [2, 2, 1, 1] is more fair than [3, 1, 1, 1]
def equationsPerThread(equations):
    
    x = np.zeros((int(threads)), dtype=int)

    for i in range(threads):
        x[i] += int(equations//threads)

    leftOver = equations%threads
    for i in range(leftOver):
        x[i] += 1

    return x

# So send the lines to each thread, using the scatter method, the master must
# check how many lines and each lines to be sent. So the master creates an array
# with length of threads, with subarray composed of the specific lines for each thread
# If the number of lines is zero, a zero is sent to the threads so that they can idle
def createSendArray(indexes, A, phase):
    
    outArr = np.zeros(len(indexes)).tolist()
    

    indexCounter = phase + 1

    for thread in range(threads):
        linesPerThread = indexes[thread]

        if linesPerThread != 0:

            idxLastLine = indexCounter + linesPerThread 
            idxRange = slice(indexCounter, idxLastLine)

            data = A[idxRange]
            outArr[thread] = data
        
        
        indexCounter = idxLastLine 

    

    return outArr

# After reciving the lines, the threads must decompress the information
# and perform the LU decomposition, line by line
def gaussLUthread(linesArr, phase, pivotLine):

    outArr = np.zeros(len(linesArr)).tolist()

    pivot = pivotLine[phase]
    i = 0

    for line in linesArr:
        outArr[i] = newLine(n, [pivotLine, line], pivot, phase)
        
        i += 1

    return outArr


"""
    Chapter 2 - Main Procedure
    ------------------------------------------------------------
"""


if rank == 0:
    
    phase = 0 # First LU Decomposition

    while True:
        equationsLeft = n - 1 - phase

        eqThreads = equationsPerThread(equationsLeft)

        pivot = A[phase][phase]

        # Check if the pivot is the smallest number is pivot colummn
        # and reorder A if necessary
        #A, pivot = pivoting(pivot, phase, A)

        debug_print(f"Next Phase: {phase}")
        debug_print (f"Pivot, : {pivot}")

        # If after pivoting, the pivot is still very small, then the process ends
        if abs(pivot) < 10**(-20):
            print("Non linear independent equations. ")
            # Send broadcast so that threads get out of the while loops
            stop = comm.bcast(True, root=0)
            debug_print(f"Stop?: {stop}")
            break
        else:
            # Threads must receive an answer, even to continue, because if not, the program doesn't continue
            stop = comm.bcast(False, root=0)
        

        scatterArr = createSendArray(eqThreads, A, phase)

        
        # Send the pivot line, the phase and the lines assigned to each thread
        out = comm.scatter(scatterArr, root=0)
        phaseCast = comm.bcast(phase, root=0)
        pivotLineCast = comm.bcast(np.array(A[phase]), root=0)

        debug_print(f"Stop?: {stop}")
        debug_print(f"Lines to be sent to each thread: {scatterArr}")

        # Perform LU decomp
        gatherArr = gaussLUthread(out, phaseCast, pivotLineCast)

       
        gatherArr = comm.gather(gatherArr, root=0)
        debug_print(f"LU decomp from each thread: {gatherArr}")


        # Mesh togheter the LU decomp from the threads and the upper lines of A already decomp.
        output =  A[0: phase+ 1]

        for threadResult in gatherArr:
            if type(threadResult) == list:
                for line in threadResult:
                    output = np.vstack((output, line))
        A = output

        debug_print(f"A|b after a single LU decomp. {A}")
        
        # Terminar se A for triangular
        if np.allclose(A, np.triu(A)):
            end = comm.bcast("end", root=0)
            debug_print(f"LU decomp finished.")
        
            break
        else:
            # As threads têm de receber uma resposta, especialmente após terminar
            end = comm.bcast("continue", root=0)

        phase += 1


else:
    while True:

        # Stops for small pivots
        stop = comm.bcast(None, root=0)
        debug_print(f"Stop? {stop}")
        if stop:
            break

        scatterArr = comm.scatter(None, root=0)
        phaseCast = comm.bcast(None, root=0)
        pivotLineCast = comm.bcast(None, root=0)

        debug_print(f"Lines to perform LU decomp: {scatterArr}")
        debug_print(f"Phase received: {phaseCast}")
        debug_print(f"Pivot line received: {pivotLineCast}")

        # Check if it has a lines to work on
        if type(scatterArr) == type(np.array(0)):
            gatherArr = gaussLUthread(scatterArr, phaseCast, pivotLineCast)
            gatherArr = comm.gather(gatherArr, root = 0)
        else:
            debug_print(f"Ordered to idle.")
            gatherArr = comm.gather(0, root = 0)

        end = comm.bcast(None, root=0)

        # LU Decomp. end check
        if end == "end":
            debug_print(f"Ordered to Stop.")
            break

# Comparison between numpy and my code.
if rank == 0 and not stop:

    print("[A|b] after LU decomp. : \n", A)
    b = A[:,-1].copy()
    A = A[:,:n]


    
    myX, stopComparison = solverLU(A, b)

    # Sometimes, after the LU decomp. the equations are not linear independent
    # This is because linear independence is not check before the LU decomp.
    if not stopComparison:
        

        mySolution = np.matmul(AInit, myX)

        npX = np.linalg.solve(AInit, bInit)

        print("My Solution of x:\n", myX)
        print("x by numpy:\n", npX.reshape((1, n)))
        print("\nTrue b: ", bInit.reshape((1,n)))
        print("\nMy Solution of b, using x: ", mySolution)
