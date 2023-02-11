from mpi4py import MPI
import time
import sys
from random import uniform
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

start_time = time.time()
n = int(sys.argv[1])
m = 0

ncores = MPI.COMM_WORLD.Get_size()



for i in range(int(round(n/ncores,0))):
    x = uniform(-1,1)
    y = uniform(-1,1)
    if x**2 + y**2 <= 1:
        m+=1
        
if rank==0:
    total_m=m
    for p in range(1, MPI.COMM_WORLD.Get_size()):
        total_m += comm.recv(source=p)
    
    ratio = (total_m/n)
    zc=1
    deltam= zc*np.sqrt(ratio*(1-ratio)/n)
    precision = len(str(ratio))-2 # Para o erro ficar com o mesmo numero de casas decimais que o ratio
    deltam = round(deltam, precision)
    
    print("\n")
    print(f"Pi is: [{4*ratio} +/- {4*deltam}]")
    print("\n")
    print(f"True value of pi is {round(np.pi,precision)}")
    if (4*(ratio-deltam) < round(np.pi,precision)) and (round(np.pi,precision) < 4*(ratio+deltam)):
        print("Value is within limits")
    else:
        print("Value is outside the limits")
    print("\n")
    
    end_time = time.time()
    real_time = end_time - start_time
    print(f"Final time: {real_time} seconds")
    print("\n")
         
else:
        
    end_time = time.time()
    real_time = end_time - start_time
    print(f"Elapsed time on core {rank} was {real_time} seconds")
    comm.send(m,dest=0)
    