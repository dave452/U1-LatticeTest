# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:12:04 2021

@author: David
"""
import numpy as np
import U1LatticeFunctions as U1
##############################################################################
###################Test#######################################################
##############################################################################
def test_plaquette(lattice_size, beta):
    lattice = U1.create_lattice(lattice_size, True)
    
    start_ind = np.array([3,3,3,3])
    directions = np.array([1,3])
    p = U1.plaquette(lattice,start_ind, directions)
    print(p)
    #print((-np.pi / 3) - (np.pi / 2))
    
def test_action(lattice_size, beta):
    lattice = U1.create_lattice(lattice_size, 0, False)
    current_ind = np.array([0,1,2,3])
    link_ind = 1
    
    S_current = U1.action_due_to_link(lattice, beta, current_ind, link_ind)
    S_0 = U1.action_full(lattice, beta)
    
    lattice[current_ind[0],current_ind[1],current_ind[2],current_ind[3]].U1_angle[link_ind] += 0.1
    
    S_new = U1.action_due_to_link(lattice, beta, current_ind, link_ind)
    S_1 = U1.action_full(lattice, beta)
    
    S_change = S_new - S_current
    S_diff = S_1 - S_0
    print(S_change - S_diff)
    
def randomise_U1_transporters(lattice):
    current = [0,0,0,0]
    for t in range(lattice.shape[0]):
        current[0] =t
        for x in range(lattice.shape[1]):   
            current[1] = x
            for y in range(lattice.shape[2]):   
                current[2] = y
                for z in range(lattice.shape[3]): 
                    current[3] = z
                    lattice[t,x,y,z].U1_angle = 2*np.pi * (np.random.rand(4) - 0.5)
                
    return lattice

def shapeOfLink(lattice_size):
    lattice = U1.create_lattice(lattice_size, 0, False)
    print(lattice[0,0,0,0].U1_angle[:].shape)