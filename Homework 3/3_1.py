"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #3 01-11-2022
    Question 1
    ============================================================

    This code is to be run on a single core.
"""
import numpy as np
import sys
import time 

"""
    Chapter 1 - Main Procedure
    ------------------------------------------------------------
"""

inputN = int(sys.argv[1])
exp = int(sys.argv[2])

timeInit = time.time()
n = inputN**exp
print(n)

m = int(np.sqrt(n))

x = np.linspace(-1, 1, m)
y = np.linspace(-1, 1, m)

sumOut = 0

for i in range(m):
    for j in range(m):
        r = x[i]**2 + y[j]**2
        if r <= 1:
            sumOut += 1

sumOut = 4*sumOut/n

timeElapsed = time.time() - timeInit
print("Value Calculated: ", sumOut)
print("Elapsed Time: ", timeElapsed)

"""
    Duração do Programa: 119 seg

    Naturalmente, este duração depende de vários fatores
    como outras aplicações abertas ou o computador ser alimentado
    por transformador ou bateria.

    No programa da folha dois, a duração foi cerca de 22.99 segundos,
    para 10**8 pontos.

    A paralelização é uma mais valia, ainda que a discretização da rede
    possa trazer maior eficiência.
"""