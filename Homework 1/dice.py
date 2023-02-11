"""
    Parallel Computing
    2022/2023 1st semester
    Exercise Sheet #1 21-09-2022
    ============================================================

    This code is to be run on a single core or thread.
"""

from random import randint
import matplotlib.pyplot as plt


"""
    Chapter 1 - Main Procedure
    ------------------------------------------------------------
"""
# Number of dice throws.
n = int(1e7)

# Dictionary to store the frequency of the sum of the faces.
D = {}

# Since its two cubes, we have to had all the possible combinations.
for i in range(2, 13):
    D[i] = 0
    
# Throw two dices for n times, then increment the corresponding sum
# in the dictionary.
for i in range(n):
    v = randint(1, 6)
    g = randint(1, 6)
    sumFaces = v + g
    # It
    D[sumFaces] += 1

"""
    Chapter 2 - Plot
    ------------------------------------------------------------
    Next, a frequency histogram will be plotted.
"""

# Transform the dict to two arrays, it's easier to plot
faces = list(D.keys())
freq = list(D.values())

# A print check for debuggin, just to be sure
print(f"Número Total de Lançamentos (Check): {sum(freq)}")

# The freq array is normalized, I think it's better present information
# relative terms.
freq = [float(i)/sum(freq) for i in freq]

plt.bar(range(len(faces)), freq, tick_label=faces)
plt.ylabel('Frequências')
plt.xlabel('Soma da Faces')
plt.title('Frequências de Lançamentos')
plt.show()


"""
    Chapter 3 - The Veredict
    ------------------------------------------------------------
    This simulation was run without the mpi API. I measured the run
    time three times:
        - 11 segundos:89 centésimos
        - 11s91
        - 11s87

    Mean Time: 11s89
"""