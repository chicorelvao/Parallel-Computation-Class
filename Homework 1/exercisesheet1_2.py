"""
Nuno Brito (nao incrito) - numero estudante 2018287967 
Tiago Azevedo - ne 2015248928

Este codigo corre a versao n core (definido quando se corre o mpirun) lancamento de dois dados. A soma dos dois dados e adicionada a um dicionario. 
O tempo que do lancamento de 10 milhoes de dados e colocado no titulo de uma figura da distribuicao que e guardada na pasta do codigo

Como esperado os dois resultados aproximam-se bastante bem da analise combinatoria. O codigo paralelizado corre muito mais rapido e podemos ver que o tempo 
se aproxima a ao tempo no single core/ (n cores usados)

"""


from mpi4py import MPI
from random import randint
import time
import matplotlib.pyplot as plt


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

ncores = MPI.COMM_WORLD.Get_size()
#ncores=8

start_time = time.time()
n= 10*10**6

D = {}
for i in range(2, 13):
    D[i] = 0
    
for i in range(int(n/ncores)):
    d1 = randint(1,6)
    d2 = randint(1,6)
    d3 = d1 + d2
    D[d3] += 1
    
for i in range(2,13):
    D[i] = D[i]/n

if rank == 0:
    for p in range(1, MPI.COMM_WORLD.Get_size()):
        Dp = comm.recv(source=p)
        for i in range(2, 13):
            D[i] += Dp[i]

    print (D)
    end_time_master = time.time()
    real_time_master = end_time_master-start_time
    plt.bar(list(D.keys()),list(D.values()))
    plt.title("Time elapsed: " + str(real_time_master) + " s")
    plt.xlabel("Sum of the two dices")
    plt.ylabel("Relative Frequency")
    plt.savefig("Multi Core Frequency Distribution.png")

else:
    comm.send(D, dest=0)

end_time = time.time()

real_time = end_time - start_time
print(f"RANK {rank} : Time elapsed: {real_time} ")
