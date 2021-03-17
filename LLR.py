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

def LLRRMUpdate(lattice, beta, dL, N_TH, N_SW,N_l, a_i, n, E_i, dE, RM = True):
    #initialise observables
    average_E = 0.
    average_accept_prob = 0.
    accept_prob = 0.
    S = U1.average_plaq(lattice) * (- 1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
    VEV_S = 0.
    #Thermalisation of the lattice
    for i in range(N_TH):
        lattice, accept_prob,S = U1.update(lattice, beta, dL, S,E_i,dE, N_l, a_i = a_i)
    print('Thermalisation Done')
    
    for i in range(N_SW):      
        #Update the lattice N_c times (find new uncorrelated configuration)
        lattice, accept_prob,S = U1.update(lattice, beta, dL, S,E_i,dE, N_l, a_i = a_i)
        VEV_S += S  
    VEV_E = VEV_S / (- 1. * (N_SW*lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
    VEV_S = ((VEV_S)/(float(N_SW))) - E_i - (dE/2.)
    if RM:
        a_i_change = (12.*VEV_S / ((n+1)* (dE ** 2.)))
    else:
        a_i_change = (12.*VEV_S / ((1)* (dE ** 2.)))

    return a_i_change, VEV_E, lattice

def LLRmain(lattice_size, beta, dL, N_B, N_TH, N_SW,N_l, N_NR, N_RM, E_MIN, E_MAX, dE,output_filename, seed = 0):
    new_seed = np.random.seed(seed)
    #open output file and output system variables
    output_file = open(output_filename, 'a')
    output_file.write('\nBEGIN')
    output_file.write('\nLattice size: [{:.0f},{:.0f},{:.0f},{:.0f}]'.format(lattice_size[0], lattice_size[1],lattice_size[2],lattice_size[3]))
    output_file.write('\nBeta:{:.5f}, N_TH:{:.5f}, N_SW:{:.5f}, N_l:{:.5f}, dTheta:{:.5f}'.format(beta,N_TH,N_SW,N_l, dL))
    output_file.write('\nN_NR:{:.5f},N_RM:{:.5f}, E_MIN:{:.5f}, E_MAX:{:.5f}, dE:{:.5f}'.format(N_NR,N_RM,E_MIN,E_MAX,dE))
    output_file.write('\nN_B:{:.5f}'.format(N_B))
    output_file.write('\nSeed: {:.0f}'.format(seed))
    output_file.close()
    a_len = int((E_MAX-E_MIN) / dE)
    a = np.ones((a_len, N_B))
    for i in range(a_len):
        for nb in range(N_B):            
            print('\nBootstrap Iteration: {:.0f}'.format(nb))
            output_file = open(output_filename, 'a')
            output_file.write('\nBootstrap Iteration: {:.0f}'.format(nb))
        
            new_seed = np.random.randint(0, 10000)
            lattice = U1.create_lattice(lattice_size, seed = new_seed)
            output_file.write('\nLattice Seed: {:.0f}'.format(new_seed))
       
            E_i = E_MIN + (float(i) * dE)
            output_file.write('\nE_{:.0f} = {:.5f}'.format(i,E_i))
        
            E_i = E_i * (-1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
            dEnew = dE * (-1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))   
                
            lattice = latticeInitialise(lattice, beta, dL, a[i,nb],dEnew,E_i)
            for nnr in range(N_NR):
                a_change, VEV_E, lattice = LLRRMUpdate(lattice, beta, dL, N_TH, N_SW,N_l, a[i,nb], nnr, E_i, dEnew, RM= False)
                a[i,nb] = a[i,nb] + a_change      
            
                print('a_i_{:.0f}: {:.3f}'.format(nnr,a[i,nb]))
                output_file.write('\na_{:.0f}_{:.0f} = {:.5f}'.format(i,nnr,a[i,nb]))
                output_file.write('\nAverage Plaquette = {:.5f}'.format(VEV_E))
            for nrm in range(N_RM):
                a_change, VEV_E, lattice = LLRRMUpdate(lattice, beta, dL, N_TH, N_SW,N_l, a[i,nb], nrm, E_i, dEnew, RM=True)
                a[i,nb] = a[i,nb] + a_change      
            
                print('a_i_{:.0f}: {:.3f}'.format(nrm + N_NR,a[i,nb]))
                output_file.write('\na_{:.0f}_{:.0f} = {:.5f}'.format(i,nrm + N_NR,a[i,nb]))
                output_file.write('\nAverage Plaquette = {:.5f}'.format(VEV_E))
            
            print('{:.0f}/{:.0f}-a_i: {:.5f} for E_i: {:.3f}'.format(i,a_len,a[i,nb],E_i))
        
            output_file.write('\na_{:.0f} = {:.5f}'.format(i,a[i,nb]))
            output_file.close()
        
    #Close files
    output_file = open(output_filename, 'a')
    output_file.write('\nEND')
    output_file.close()
    return a


def latticeInitialise(lattice, beta, dL, a_i, dE, E_i):    
    print(a_i)
    for i in range(100):
        lattice, accept_prob, S = U1.update(lattice, beta, dL, N_l = 1, a_i = a_i)
        #print('{:.0f}/{:.0f}-Acceptance Probability: {:.3f}'.format(i+1,N_TH,accept_prob))
    print('Initialisation Part 1: Done')
    S = U1.average_plaq(lattice) * (- 1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
    init = True
    thermcount = 0
    while init:
        thermcount += 1
        lattice, accept_prob, S = U1.update(lattice, beta, dL,S=S, a_i = a_i)
        init = (np.abs(S) >= np.abs(E_i + dE)) or (np.abs(S) <= np.abs(E_i))    
        if ((thermcount % 100) == 0):
            print(S / (-1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6)))
            print(thermcount)
            # if(thermcount % 1000 == 0):
            #     lattice = latticeInitialise(lattice, beta, dL, a_i, dE, E_i)
            #     init = False
    print('Initialisation Part 2: Done, After :', thermcount, 'steps')
    return lattice

def timerFunction():
    #a_change, VEV_E = LLRRMUpdate(lattice_size, beta, dL, N_TH, N_SW,N_l, a_i, n, E_i, dE, new_seed)
    lattice_size = [4,4,4,4]
    beta = 1
    dL = np.pi / 2.5
    N_l = 10
    lattice = U1.create_lattice(lattice_size)
    %timeit U1.update(lattice, beta, dL, N_l= N_l)
    
    
    
lattice_size = [4,4,4,4]
beta = 1
dL = np.pi / 2.5
 # standard deviation of the change
N_B = 2
N_TH = 100 # thermalisation steps
N_SW = 200 # number of oberservations 
N_l = 2
N_RM = 50
N_NR = 30
E_MIN = 0.59
E_MAX = 0.62
dE = 0.01
seed = 987

filename = './output/RM'+str(lattice_size[0])+str(lattice_size[1])+str(lattice_size[2])+str(lattice_size[3])+'b'+str(beta)+'s'+str(seed) + '.txt'
a = LLRmain(lattice_size, beta, dL, N_B, N_TH, N_SW,N_l,N_NR, N_RM, E_MIN, E_MAX, dE, filename,seed)
print(a)
#timerFunction()
#a_i = 1
#n =0
#%timeit timerFunction(lattice_size, beta, dL, N_TH, N_SW,N_l,a_i, n , E_MIN, dE, seed)

