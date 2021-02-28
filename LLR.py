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

def LLRRMUpdate(lattice_size, beta, dL, N_TH, N_SW,N_l, a_i, n, E_i, dE, seed):
    #initialise lattice
    lattice = U1.create_lattice(lattice_size, seed = seed)
    E_i = E_i * (-1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
    dE = dE * (-1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
    print('Seed: {:.0f}'.format(seed))
    #initialise observables
    average_E = 0.
    average_accept_prob = 0.
    accept_prob = 0.
    S = 0.
    VEV_S = 0.
    #Thermalisation of the lattice
    for i in range(N_TH):
        lattice, accept_prob, dS = U1.update(lattice, beta, dL, a_i = a_i)
        print('{:.0f}/{:.0f}-Acceptance Probability: {:.3f}'.format(i+1,N_TH,accept_prob))
        average_accept_prob += accept_prob
    
    S = U1.average_plaq(lattice) * (- 1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
    init = True
    while init:
        lattice, accept_prob, dS = U1.update(lattice, beta, dL, a_i = a_i)
        S += (dS)
        init = (np.abs(S) >= np.abs(E_i + dE)) or (np.abs(S) <= np.abs(E_i))  
        print(np.abs(S))
        print(np.abs(E_i + dE))
        print(np.abs(E_i))
        print((S / (- 1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))))
        
    for i in range(N_SW):      
        #Update the lattice N_c times (find new uncorrelated configuration)
        lattice, accept_prob,dS = U1.update(lattice, beta, dL/4., S,E_i,dE, N_l, a_i = a_i)
        print('{:.0f}/{:.0f}-Acceptance Probability: {:.3f}'.format(i+1,N_SW,accept_prob))
        S += (dS)
        average_plaquette = (S / (- 1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6)))
        print('{:.0f}/{:.0f}-Average Plaquette: {:.5f}'.format(i+1,N_SW,average_plaquette))
        #Add current average plaquette to total average plaquette
        VEV_S += S
    #Thermalsation complete
    VEV_S = ((VEV_S)/(float(N_SW))) - E_i - (dE/2.)
    print("Average E: ",VEV_S)
    a_i_change = (12.*VEV_S / ((n+1)* (dE ** 2.)))
    print("a_i change :", a_i_change)
    return a_i_change

def LLRmain(lattice_size, beta, suggested_change, N_TH, N_SW,N_l, N_RM, E_MIN, E_MAX, dE, seed = 0):
    a_len = int((E_MAX-E_MIN) / dE)
    a = np.ones(a_len)
    for i in range(a_len):
        E_i = E_MIN + (float(i) * dE)
        for n in range(N_RM):
            a_change = LLRRMUpdate(lattice_size, beta, suggested_change, N_TH, N_SW,N_l, a[i], n, E_i, dE, seed)
            a[i] = a[i] + a_change
            print('a_i_{:.0f}: {:.3f}'.format(n,a[i]))
        print('{:.0f}/{:.0f}-a_i: {:.3f}'.format(i,a_len,a[i]))
    return a


lattice_size = [4,4,4,4]
beta = 0.95
dL = np.pi / 2.5
 # standard deviation of the change
N_TH = 200 # thermalisation steps
N_SW = 100 # number of oberservations 
N_l = 1
N_RM = 10
E_MIN = 0.50
E_MAX = 0.55
dE = 0.01
seed = 1
a = LLRmain(lattice_size, beta, dL, N_TH, N_SW,N_l, N_RM, E_MIN, E_MAX, dE, seed = 294)
print(a)