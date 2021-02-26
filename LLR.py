# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 10:03:13 2021

@author: David
"""

import numpy as np
import U1LatticeFunctions as U1
import U1LatticeTestFunctions as U1Test
#Defines a Lattice sizes  
#N = [Lattice Size Time, L.S x, L.S y, L.S z]
def LLRRMUpdate(lattice_size, beta, suggested_change, N_TH, N_SW, a_i, n, E_i, dE, seed = 0):
    #initialise lattice
    lattice = U1.create_lattice(lattice_size, seed = seed)
    print('Seed: {:.0f}'.format(seed))
    #initialise observables
    average_E = 0.
    average_accept_prob = 0.
    accept_prob = 0.

    #Thermalisation of the lattice
    for i in range(N_TH):
        init = True
        while init:
            lattice, accept_prob = U1.update(lattice,beta*a_i, suggested_change)
            E = U1.average_plaq(lattice)*beta 
            init = (E >= (E_i + dE)) or (E <= (E_i))
            print(E)
        print('{:.0f}/{:.0f}-Acceptance Probability: {:.3f}'.format(i+1,N_TH,accept_prob))
        average_accept_prob += accept_prob
    #Thermalsation complete
    average_accept_prob = average_accept_prob / N_TH
    print('Average Acceptance Probability: {:.3f}'.format(average_accept_prob))
    
    #Make N_SW observations
    for i in range(N_SW):
        init = True
        while init:
            lattice, accept_prob = U1.update(lattice, beta*a_i, suggested_change)
            E = U1.average_plaq(lattice)*beta 
            init = (E >= (E_i + dE)) or (E <= (E_i))                          
        print(E)  
        average_E = average_E + E   
    average_E = (average_E / float(N_SW)) - E_i - (dE/2.)
    print("Average E: ",average_E)
    a_i_change = (12.*average_E / ((n+1)* (dE ** 2.)))
    if a_i_change > 1.:
        print("ERROR")
        a_i_change = 0.
    return a_i_change

def LLRRMUpdate2(lattice_size, beta, suggested_change, N_TH, N_SW, a_i, n, E_i, dE, seed = 0):
    #initialise lattice
    lattice = U1.create_lattice(lattice_size, seed = seed)
    oldlattice = lattice
    print('Seed: {:.0f}'.format(seed))
    #initialise observables
    average_E = 0.
    average_accept_prob = 0.
    accept_prob = 0.

    #Thermalisation of the lattice
    init = True
    while init:
        lattice, accept_prob = U1.update(lattice, beta*a_i, suggested_change)
        E = U1.average_plaq(lattice)*beta 
        init = (E >= (E_i + dE)) or (E <= (E_i))  
        if(not init):
            oldlattice = lattice 
    i = 0
    while i < N_TH:
        lattice, accept_prob = U1.update(lattice, beta*a_i, suggested_change)
        E = U1.average_plaq(lattice)*beta
        init = (E >= (E_i + dE)) or (E <= (E_i)) 
        if(init):
            lattice = oldlattice
        else:
            oldlattice = lattice 
            i += 1
            average_accept_prob += accept_prob
            print(i)
    #Thermalsation complete
    average_accept_prob = average_accept_prob / N_TH
    print('Average Acceptance Probability: {:.3f}'.format(average_accept_prob))
    
    #Make N_SW observations
    i = 0
    while i < N_SW:
        lattice, accept_prob = U1.update(lattice, beta*a_i, suggested_change)
        E = U1.average_plaq(lattice)*beta 
        init = (E >= (E_i + dE)) or (E <= (E_i))  
        if(init):
            lattice = oldlattice
        else:
            oldlattice = lattice                          
            average_E = average_E + E 
            i+= 1
            print(i)
    average_E = (average_E / float(N_SW)) - E_i - (dE/2.)
    print("Average E: ",average_E)
    a_i_change = (12.*average_E / ((n+1)* (dE ** 2.)))
    if a_i_change > 1.:
        print("ERROR a_i_change =",a_i_change)
        a_i_change = 0.
    return a_i_change

def LLRmain(lattice_size, beta, suggested_change, N_TH, N_SW, N_RM, E_MIN, E_MAX, dE, seed = 0):
    a_len = int((E_MAX-E_MIN) / dE)
    a = np.ones(a_len)
    for i in range(a_len):
        E_i = E_MIN + (float(i) * dE)
        for n in range(N_RM):
            a_change = LLRRMUpdate2(lattice_size, beta, suggested_change, N_TH, N_SW, a[i], n, E_i, dE, seed)
            a[i] = a[i] + a_change
            print('a_i_{:.0f}: {:.3f}'.format(n,a[i]))
        print('{:.0f}/{:.0f}-a_i: {:.3f}'.format(i,a_len,a[i]))
    return a


lattice_size = [4,4,4,4]
beta = 0.95
suggested_change = np.pi / 2.5
 # standard deviation of the change
N_TH = 10 # thermalisation steps
N_SW = 100 # number of oberservations 
N_RM = 10
E_MIN = 0.519
E_MAX = 0.521
dE = 0.0002
seed = 1
a = LLRmain(lattice_size, beta, suggested_change, N_TH, N_SW, N_RM, E_MIN, E_MAX, dE, seed = 294)
print(a)