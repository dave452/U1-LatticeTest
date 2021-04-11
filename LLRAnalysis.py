# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 15:21:51 2021

@author: David
"""
import matplotlib.pyplot as plt
import numpy as np
def grabValues(filename, N_NR, bool_plot):
    file = open(filename)
    
    a_i = []
    A = [[]]
    A.clear()
    E = []
    i = 0 
    j = -1
    line = file.readline()
    count = []
    count.append(0)
    while line[:3] != 'END':
        str_ai_value = 'a_' + str(j) + '_' + str(i) + ' ='
        str_next = 'E_' + str(j+1) + ' ='
        str_restart = 'BEGIN'
        str_plaq = 'Average Plaquette ='
        str_bootstrap = 'Bootstrap Iteration:' 
        if line[:len(str_next)] == str_next:              
            if (i > 0):
                count.append(i + count[len(count) - 1])
                i = 0                
                A.extend(a_i) 
                a_i.clear()
            E.append(float(line[len(str_next)+1:])) 
            j += 1            
        elif line[:len(str_restart)] == str_restart:
            if(j >= 0):
                count.append(i + count[len(count) - 1])
                i = 0
                j = -1
                A.extend(a_i)           
                a_i.clear()               
        elif line[:len(str_ai_value)] == str_ai_value:
             a_i.append(float(line[len(str_ai_value)+1:]))             
             i += 1         
        elif line[:len(str_bootstrap)] == str_bootstrap:
            if float(line[len(str_bootstrap)+1:]) > 0:
                count.append(i + count[len(count) - 1])
                j -=1
        line = file.readline()
    file.close()
    count.append(i + count[len(count) - 1])
    A.extend(a_i)
    
    mean_final_a_i = []
    mfa = 0.
    E = np.array(E)
    E_unique = []
    colours = ['b','g','r','c','m','y']
    for e in E:
        if e not in E_unique:
            E_unique.append(e)
    for e in E_unique:
        mfa = 0.
        indices = np.where(E==e)
        c = 0
        for i in indices[0]:
            if(bool_plot):
                plt.plot( range(count[i+1] - count[i]),A[count[i]:count[i+1]])
            mfa += A[count[i+1]-1]
            c += 1
        mfa /= c
        mean_final_a_i.append(mfa)
        if(bool_plot):
            plt.title('E_i = ' + str(e))
            plt.axvline(N_NR,color ='k', linestyle = '--')
            plt.show()
    return E_unique, mean_final_a_i
def plota(filename, N_NR, plot):
    E_unique, mean_final_a_i = grabValues(filename, N_NR, plot)
    if not plot:    
        plt.plot(E_unique, -1. * np.array(mean_final_a_i), 'bx')


N_NR = 10
files = ['./output/Cluster/RM4444E0.47.txt','./output/Cluster/RM4444E0.48.txt',
         './output/Cluster/RM4444E0.49.txt',
         './output/Cluster/RM4444E0.50.txt','./output/Cluster/RM4444E0.51.txt',
         './output/Cluster/RM4444E0.52.txt','./output/Cluster/RM4444E0.53.txt',
         './output/Cluster/RM4444E0.54.txt','./output/Cluster/RM4444E0.55.txt',
         './output/Cluster/RM4444E0.56.txt',
         './output/Cluster/RM4444E0.57.txt', './output/Cluster/RM4444E0.58.txt',
         './output/Cluster/RM4444E0.59.txt', './output/Cluster/RM4444E0.60.txt',
         './output/Cluster/RM4444E0.61.txt', './output/Cluster/RM4444E0.62.txt',
         './output/Cluster/RM4444E0.63.txt', './output/Cluster/RM4444E0.64.txt',
         './output/Cluster/RM4444E0.65.txt', './output/Cluster/RM4444E0.66.txt']

for file in files:
    plota(file, N_NR, True)

for file in files:
    plota(file, N_NR, False)