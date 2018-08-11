import random
import numpy as np
import scipy.stats


realmean = 0
learnedmean = 0
realstd = 0
learnedstd = 0
data = 0

numtests = 10000

realmean = random.randint(1,10)
realstd = random.randint(1,10)

print("real")
print(realmean)
print(realstd)

for i in range(numtests):
    data = np.random.normal(realmean,realstd)
    if(i == 0):
        learnedmean = data
    elif(i == 1):
        oldmean = learnedmean
        learnedmean = (oldmean+data)/(i+1)
        learnedstd = np.std((oldmean,data),ddof=1)
    else:
        learnedstd = np.sqrt(((i-1)/i)*(learnedstd**2)+((1/(i+1))*((data-learnedmean)**2)))
        learnedmean = learnedmean + ((data-learnedmean)/(i+1))

        
print("learned")
print(learnedmean)
print(learnedstd)
