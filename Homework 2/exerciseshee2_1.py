import sys
from random import uniform
import time
import numpy as np


start_time = time.time()

n = int(sys.argv[1])
m = 0



for i in range(n):
    x = uniform(-1,1)
    y = uniform(-1,1)
    if x**2+y**2 < 1:
        m = m + 1 
      
ratio = m/n
zc=1

deltam= zc*np.sqrt(ratio*(1-ratio)/n)
precision = len(str(ratio))-2 # Para o erro ficar com o mesmo numero de casas decimais que o ratio
deltam = round(deltam, precision)
    
end_time = time.time()

real_time = end_time - start_time    


print("\n")
print(f"Pi is: [{4*ratio} +/- {4*deltam}]")
print("\n")
print(f"True value of pi is {round(np.pi,precision)}")
if (4*(ratio-deltam) < round(np.pi,precision)) and (round(np.pi,precision) < 4*(ratio+deltam)):
    print("Value is within limits")
else:
    print("Value is outside the limits")

print("\n")
print(f"Time elapsed: {real_time} seconds")
print("\n")