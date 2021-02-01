# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:55:41 2021

@author: David
"""

import numpy as np
import matplotlib.pyplot as plt

def findPlaq(filename, N_obs, N_ends):
    file = open(filename)
    Plaq = np.zeros((N_obs, N_ends))
    line = file.readline()
    
    for j in range(N_ends):
        i = 0
        while line[:3] != 'END':
            if(line[:19] == 'Average Plaquette: '):
                Plaq[i,j] = float(line[19:])
                i += 1
            line = file.readline()
        line = file.readline()
    file.close()
    print(i)
    print(filename, 'complete')
    return Plaq

files = np.array(["./output/4666b1s4565.txt"])
N_obs = 10000
N_seeds = files.shape[0]
N_ends = 1
full_Plaq = np.zeros((N_obs, N_ends))
full_Plaq[:,:] = findPlaq(files[0], N_obs, N_ends)
plt.hist(full_Plaq.flatten(),bins =100, density=True)
plt.show()
print(full_Plaq.mean(axis = 0))
print(full_Plaq.std(axis = 0))
for i in range(N_ends):
    plt.plot(full_Plaq[:,i], range(N_obs))
    plt.title(i)
    plt.show()