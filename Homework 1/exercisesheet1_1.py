"""
Nuno Brito (nao incrito) - numero estudante 2018287967 
Tiago Azevedo - ne 2015248928
Este codigo corre a versao single core do lancamento de dois dados. A soma dos dois dados e adicionada a um dicionario e no final faz print
aos valores obtidos e ao erro relativo em relacao aos resultados da combinatoria.
O tempo do lancamento de 10 milhoes de dados e colocado no titulo de uma figura da distribuicao que e guardada na pasta do codigo

"""




from random import randint
import time
import matplotlib.pyplot as plt

time_start = time.time()

n= 10*10**6

comb = {2:round(1/36,4) , 3: round(2/36,4), 4:round(3/36,4), 5:round(4/36,4), 6 : round(5/36,4), 7: round(6/36,4), 8 : round(5/36,4), 9 : round(4/36,4), 10: round(3/36,4), 11 : round(2/36,4), 12:round(1/36,4) }
D = {}

for i in range(2,13):
    D[i] = 0
    
for j in range(n):
    d1 = randint(1,6)
    d2 = randint(1,6)
    d3 = d1 + d2
    D[d3] += 1
    
for i in range(2,13):
    D[i] = round(D[i]/n,4)   
    
time_end = time.time()
real_time = time_end - time_start

ERRO = D.copy()

for i in list(ERRO.keys()):
    ERRO[i] = round(abs((D[i]-comb[i]))/comb[i]*100,4)
    print(comb[i])

print(ERRO)
print(f"Time elapsed: {real_time} ")

plt.bar(list(D.keys()),list(D.values()))
plt.xlabel("Sum of the two dices")
plt.ylabel("Relative Frequency")
plt.title("Time elapsed: " + str(real_time) + " s")
plt.savefig("Single Core Frequency Distribution.png")

print("Expected relative frequency: " + str(comb))
print("\n")
print("Obtained relative frequency: " + str(D))
print("\n")
print("Relative Error %: " + str(ERRO))



