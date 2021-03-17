# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 15:21:51 2021

@author: David
"""
import matplotlib.pyplot as plt
import numpy as np
def plota(filename):
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
            plt.plot( range(count[i+1] - count[i]),A[count[i]:count[i+1]])
            mfa += A[count[i+1]-1]
            c += 1
        mfa /= c
        mean_final_a_i.append(mfa)
        plt.title('E_i = ' + str(e))
        plt.show()
        
    plt.plot(E_unique, mean_final_a_i, 'kx')

def poop():
    P = []
    A = []
    B = []
    A.append([0,1])
    A.append([1,2])
    P.extend(A)
    print(P)
    A.clear()
    A.append([3,4,5])
    P.extend(A)
    print(P)
    A.clear()
    A.append([4])
    P.extend(A)
    print(P)


filenames = './output/RM4444b1s98.txt'
plota(filenames)