%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd
import time
from math import *
import numpy as np

fiatAmount = 1000
actualPrice = [1500.0]
increaseCryptoRef = 400.0
decreaseCryptoRef = -200.0

for i in range(100):
    actualPrice.append(actualPrice[-1]+increaseCryptoRef)
    actualPrice.append(actualPrice[-1]+decreaseCryptoRef)

print("départ : ",fiatAmount," USDT")
data = []
i=0
remember=0

for price in actualPrice[1:-1]:
    i+=1
    if(i % 2 != 0):
        benefice = price/actualPrice[i-1]
    else:
        benefice = actualPrice[i+1]/price
    
    if remember==benefice:
        continue
    fiatAmount = fiatAmount*benefice
    data = np.append(data,fiatAmount)
    remember = benefice
    
df = pd.DataFrame(data,columns=["wallet"])
figure=plt.figure()
plt.title("Evolution de la start 200/400")
plot2 = plt.plot(range(df.size), df, color="green", linestyle="dashed")

ax = plt.axes()
ax = ax.set(xlabel="Temps",ylabel="Nb USDT")
df