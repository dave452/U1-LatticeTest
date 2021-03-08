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
    A = []
    e_i = []
    E = []
    i = 0 
    j = 0
    line = file.readline()
    while line[:3] != 'END':
        str_ai_value = 'a_' + str(j) + '_' + str(i) + ' ='
        str_ai_next = 'a_' + str(j+1) + '_0' + ' ='
        str_plaq = 'Average Plaquette ='
        if line[:len(str_ai_value)] == str_ai_value:
             a_i.append(float(line[len(str_ai_value)+1:]))
             
             i += 1
             
        elif line[:len(str_plaq)] == str_plaq:
            e_i.append(float(line[len(str_plaq)+1:]))
        elif  line[:len(str_ai_next)] == str_ai_next:
            print(i)
            plt.plot( range(i),a_i)
            plt.title('E_i' + str(np.mean(e_i)))
            plt.show()
            i = 1
            j += 1
            A.append(a_i)
            E.append(e_i)
            a_i.clear()
            e_i.clear()
            a_i.append(float(line[len(str_ai_next)+1:]))
        line = file.readline()
    file.close()
    print(i)
    plt.plot( range(i),a_i)
    plt.title('E_i' + str(np.mean(e_i)))
    plt.show()
    A.append(a_i)
    E.append(e_i)
    print(j)
    

filenames = './output/RM4444b1.0s76.txt'
plota(filenames)    