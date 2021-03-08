# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 10:03:13 2021

@author: David
"""

import numpy as np
import U1LatticeFunctions as U1
import U1LatticeTestFunctions as U1Test
import timeit
#Defines a Lattice sizes  
#N = [Lattice Size Time, L.S x, L.S y, L.S z]

def LLRRMUpdate(lattice_size, beta, dL, N_TH, N_SW,N_l, a_i, n, E_i, dE, seed):
    #initialise lattice
    lattice = U1.create_lattice(lattice_size, seed = seed)
    E_i = E_i * (-1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
    dE = dE * (-1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
    #print('Seed: {:.0f}'.format(seed))
    #initialise observables
    average_E = 0.
    average_accept_prob = 0.
    accept_prob = 0.
    S = 0.
    VEV_S = 0.
    #Thermalisation of the lattice
    for i in range(N_TH):
        lattice, accept_prob, S = U1.update(lattice, beta, dL, a_i = a_i)
        #print('{:.0f}/{:.0f}-Acceptance Probability: {:.3f}'.format(i+1,N_TH,accept_prob))
        average_accept_prob += accept_prob
    print('Thermalisation Done')
    S = U1.average_plaq(lattice) * (- 1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
    init = True
    thermcount = 0
    while init:
        thermcount += 1
        lattice, accept_prob, S = U1.update(lattice, beta, dL,S=S, a_i = a_i)
        init = (np.abs(S) >= np.abs(E_i + dE)) or (np.abs(S) <= np.abs(E_i))  
    #print('Thermalisation Complete, S =',S)    
    print('Thermalisation 2 Done', thermcount)
    for i in range(N_SW):      
        #Update the lattice N_c times (find new uncorrelated configuration)
        lattice, accept_prob,S = U1.update(lattice, beta, dL, S,E_i,dE, N_l, a_i = a_i)
        #print('{:.0f}/{:.0f}-Acceptance Probability: {:.3f}'.format(i+1,N_SW,accept_prob))
        average_plaquette = (S / (- 1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6)))
        #print('{:.0f}/{:.0f}-Average Plaquette: {:.5f}'.format(i+1,N_SW,average_plaquette))
        #Add current average plaquette to total average plaquette
        VEV_S += S
    #Thermalsation complete
    
    VEV_E = VEV_S / (- 1. * (N_SW*lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
    VEV_S = ((VEV_S)/(float(N_SW))) - E_i - (dE/2.)
    #print("Average E: ",VEV_S)
    a_i_change = (12.*VEV_S / ((n+1)* (dE ** 2.)))
    #print("a_i change :", a_i_change)
    return a_i_change, VEV_E

def LLRmain(lattice_size, beta, dL, N_TH, N_SW,N_l, N_RM, E_MIN, E_MAX, dE,output_filename, seed = 0):
    np.random.seed(seed)
    #open output file and output system variables
    output_file = open(output_filename, 'a')
    output_file.write('\nBEGIN')
    output_file.write('\nLattice size: [{:.0f},{:.0f},{:.0f},{:.0f}]'.format(lattice_size[0], lattice_size[1],lattice_size[2],lattice_size[3]))
    output_file.write('\nBeta:{:.5f}, N_TH:{:.5f}, N_SW:{:.5f}, N_l:{:.5f}, dTheta:{:.5f}'.format(beta,N_TH,N_SW,N_l, dL))
    output_file.write('\nN_RM:{:.5f}, E_MIN:{:.5f}, E_MAX:{:.5f}, dE:{:.5f}'.format(N_RM,E_MIN,E_MAX,dE))
    output_file.write('\nSeed: {:.0f}'.format(seed))
    
    a_len = int((E_MAX-E_MIN) / dE)
    a = np.ones(a_len)
    for i in range(a_len):
        E_i = E_MIN + (float(i) * dE)
        output_file.write('\nE_{:.0f} = {:.5f}'.format(i,E_i))
        for n in range(N_RM):
            new_seed = np.random.randint(0,10000)
            output_file.write('\nLattice Seed: {:.0f}'.format(new_seed))
            a_change, VEV_E = LLRRMUpdate(lattice_size, beta, dL, N_TH, N_SW,N_l, a[i], n, E_i, dE, new_seed)
            a[i] = a[i] + a_change
            
            print('a_i_{:.0f}: {:.3f}'.format(n,a[i]))
            output_file.write('\na_{:.0f}_{:.0f} = {:.5f}'.format(i,n,a[i]))
            output_file.write('\nAverage Plaquette = {:.5f}'.format(VEV_E))
        print('{:.0f}/{:.0f}-a_i: {:.5f} for E_i: {:.3f}'.format(i,a_len,a[i],E_i))
        output_file.write('\na_{:.0f} = {:.5f}'.format(i,a[i]))
    #Close files
    output_file.write('\nEND')
    output_file.close()
    return a

def timerFunction(lattice_size, beta, dL, N_TH, N_SW,N_l,a_i, n , E_i, dE, new_seed):
    a_change, VEV_E = LLRRMUpdate(lattice_size, beta, dL, N_TH, N_SW,N_l, a_i, n, E_i, dE, new_seed)
    
    
    
    
lattice_size = [4,4,4,4]
beta = 1.0
dL = np.pi / 2.5
 # standard deviation of the change
N_TH = 50 # thermalisation steps
N_SW = 100 # number of oberservations 
N_l = 1
N_RM = 50
E_MIN = 0.57
E_MAX = 0.60
dE = 0.01
seed =76

filename = './output/RM'+str(lattice_size[0])+str(lattice_size[1])+str(lattice_size[2])+str(lattice_size[3])+'b'+str(beta)+'s'+str(seed) + '.txt'
a = LLRmain(lattice_size, beta, dL, N_TH, N_SW,N_l, N_RM, E_MIN, E_MAX, dE, filename,seed)
print(a)

#a_i = 1
#n =0
#%timeit timerFunction(lattice_size, beta, dL, N_TH, N_SW,N_l,a_i, n , E_MIN, dE, seed)

