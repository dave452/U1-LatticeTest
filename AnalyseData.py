# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:55:41 2021

@author: David
"""

import numpy as np
import matplotlib.pyplot as plt

def findPlaq(filename, N_obs):
    file = open(filename)
    Plaq = np.zeros((N_obs))
    line = file.readline()
    i = 0
    while line[:3] != 'END':
        if(line[:19] == 'Average Plaquette: '):
            Plaq[i] = float(line[19:])
            i += 1
        line = file.readline()
    file.close()
    print(i)
    print(filename, 'complete')
    return Plaq

files = np.array(["output_file1.txt","output_file2.txt","output_file3.txt","output_file4.txt"])
N_obs = 250
N_seeds = files.shape[0]
full_Plaq = np.zeros((N_obs, N_seeds))
for i in range(N_seeds):
    full_Plaq[:,i] = findPlaq(files[i], N_obs)
plt.hist(full_Plaq.flatten(), density=True)
print(full_Plaq.flatten().mean())
print(full_Plaq.flatten().std())