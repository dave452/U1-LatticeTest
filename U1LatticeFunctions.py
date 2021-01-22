# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:10:59 2021

@author: David
"""

import numpy as np

##############################################################################
########################Lattice Class#########################################
##############################################################################

class latticePoint :
    def __init__(self, pos, U1_t) :
        #Position 4 vector
        #U1_angle 4 vector with components as between -pi and pi
        self.position = pos
        self.U1_angle = U1_t

##############################################################################
####################### Functions on lattice #################################
##############################################################################
def moveOnLattice(lattice, current_ind, move, move_ind):
    #Takes in the entire lattice, the index of the current position and the index of the planned move
    #Returns the index of the new lattice point and the change in field for that move
    #Move will be all 0 except a 1 or -1 in the direction of travel
    
    #current_ind = np.array(current_ind)
    #move = np.array(move)
           
    #Define variables that will be output
    U1_move_strength = 0.
    new_ind = current_ind + move
    
    #Periodic boundary conditions
    if(new_ind[move_ind] >= lattice.shape[move_ind]):
            new_ind[move_ind] = 0
    if(new_ind[move_ind] < 0):
            new_ind[move_ind] = (lattice.shape[move_ind] - 1)

    #Gets the strength in field strength from lattice array
    if(move[move_ind] > 0): 
        U1_move_strength = lattice[current_ind[0],current_ind[1],current_ind[2],current_ind[3]].U1_angle[move_ind]
    elif(move[move_ind] < 0):
        U1_move_strength = -lattice[new_ind[0],new_ind[1],new_ind[2],new_ind[3]].U1_angle[move_ind]
    else: print("Clearly a problem here 0")
    
    return new_ind, U1_move_strength

def plaquette(lattice,start_ind, directions):
    #start_ind is the index of the start of the plaquette
    #direction is a 1D array containing the indices of the directions of the movement
    #Movement in first direction 
    
    current_ind = start_ind
    move_0 = np.array([0,0,0,0])
    move_0[directions[0]] = 1 
    #move_0[directions[0]] = np.random.choice([-1,1])
    
    #Movement in second direction
    move_1 = np.array([0,0,0,0])
    move_1[directions[1]] = 1
    #move_1[directions[1]] = np.random.choice([-1,1])
    
    #Calculate plaquette angle
    U1_field_change = np.array([0.,0.,0.,0.])
    #print(current_ind, move_0)
    current_ind, U1_field_change[0] = moveOnLattice(lattice,current_ind, move_0, directions[0])
    #print(U1_field_change[0])
    #print(current_ind, move_1)
    current_ind, U1_field_change[1] = moveOnLattice(lattice,current_ind, move_1, directions[1])
    #print(U1_field_change[1])
    #print(current_ind, -move_0)
    current_ind, U1_field_change[2] = moveOnLattice(lattice,current_ind, -move_0,directions[0])
    #print(U1_field_change[2])
    #print(current_ind, - move_1)
    current_ind, U1_field_change[3] = moveOnLattice(lattice,current_ind, -move_1,directions[1])
    #print(U1_field_change[3])
    #print(current_ind)
    
    return U1_field_change.sum()
    
def action_full(lattice, beta):
    #Calculates the action for the lattice in full for the current field configuration
    S = 0
    start = [0,0,0,0]
    directions = [0,0]
    for t in range(lattice.shape[0]):
        start[0] =t
        for x in range(lattice.shape[1]):   
            start[1] = x
            for y in range(lattice.shape[2]):   
                start[2] = y
                for z in range(lattice.shape[3]): 
                    start[3] = z
                    for mu in range(4):
                        directions[0] = mu
                        for nu in range(mu+1,4):      
                            directions[1] = nu
                            S+= np.cos(plaquette(lattice,start, directions))
    S *= - beta
    return S

def average_plaq(lattice, beta):
    #Calculates the plaquette for the lattice in full for the current field configuration
    S = 0
    start = [0,0,0,0]
    directions = [0,0]
    for t in range(lattice.shape[0]):
        start[0] =t
        for x in range(lattice.shape[1]):   
            start[1] = x
            for y in range(lattice.shape[2]):   
                start[2] = y
                for z in range(lattice.shape[3]): 
                    start[3] = z
                    for mu in range(4):
                        directions[0] = mu
                        for nu in range(mu+1,4):      
                            directions[1] = nu
                            S+= np.cos(plaquette(lattice,start, directions))
    S = S / (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6)
    return S

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

def polykov_loop(lattice, start_ind):
    move = np.array([1,0,0,0])
    current_ind = start_ind
    field_change = 0.
    field_total = 0.
    for i in range(lattice.shape[0]):
        current_ind, field_change = moveOnLattice(lattice, current_ind, move, 0)
        field_total += field_change
    return field_total

def action_due_to_link(lattice,beta,current_ind, link_ind):
    S = 0       
    for i in range(4):
        if(link_ind != i):
            S +=  np.cos(plaquette(lattice,current_ind, [link_ind,i]))
            temp_ind = np.array([0,0,0,0])
            temp_ind[i] = -1
            temp_ind, U1temp = moveOnLattice(lattice, current_ind, temp_ind, i)
            S += np.cos(plaquette(lattice,temp_ind, [link_ind,i]))
    S *= - beta
    return S


def change_link(lattice,beta, link_change, current_ind, link_ind):    
    S_current = action_due_to_link(lattice, beta, current_ind, link_ind)
    lattice[current_ind[0],current_ind[1],current_ind[2],current_ind[3]].U1_angle[link_ind] += link_change
    S_new = action_due_to_link(lattice, beta, current_ind, link_ind)
    S_change = S_new - S_current
    activ_prob = np.exp(-S_change)
    accept = (np.random.rand() < activ_prob)
    if(not accept):
        S_change = 0
        lattice[current_ind[0],current_ind[1],current_ind[2],current_ind[3]].U1_angle[link_ind] -= link_change
    return accept, S_change, lattice

def update(lattice, beta, suggested_change):
    #Calculates the action for the lattice in full for the current field configuration
    start = [0,0,0,0]
    accept_prob = 0.
    for t in range(lattice.shape[0]):
        start[0] =t
        for x in range(lattice.shape[1]):   
            start[1] = x
            for y in range(lattice.shape[2]):   
                start[2] = y
                for z in range(lattice.shape[3]): 
                    start[3] = z
                    for mu in range(4):
                          accept, S_change, lattice = change_link(lattice,beta,np.random.normal(0., suggested_change), start, mu)
                          if(accept):
                              accept_prob += 1.
    accept_prob = accept_prob / (4 * lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3])
    return lattice, accept_prob 
   

def create_lattice(lattice_size, seed = 0, test = False):
    print(seed)
    np.random.seed(seed)
    if(not test):        
        lattice = np.array([latticePoint([float(t),float(x),float(y),float(z)], 
                                         2*np.pi * (np.random.rand(4) - 0.5))
                            for t in range(lattice_size[0]) for x in range(lattice_size[1])
                            for y in range(lattice_size[2]) for z in range(lattice_size[3])])
    else:
        lattice = np.array([latticePoint([float(t),float(x),float(y),float(z)], 
                                         (np.array([float(t)/2, float(x)/3, float(y)/4, float(z)/5]) * np.pi))
        for t in range(lattice_size[0]) for x in range(lattice_size[1])
        for y in range(lattice_size[2]) for z in range(lattice_size[3])])
        
    lattice.shape = lattice_size
    return lattice

def main(lattice_size, beta, suggested_change, N_t, N_c, N_o, output_filename, seed = 0):
    lattice = create_lattice(lattice_size, seed = seed)
    output_file = open(output_filename, 'a')
    
    output_file.write('\nBEGIN')
    output_file.write('\nLattice size: [{:.0f},{:.0f},{:.0f},{:.0f}]'.format(lattice_size[0], lattice_size[1],lattice_size[2],lattice_size[3]))
    output_file.write('\nBeta:{:.5f}, N_t:{:.5f}, N_c:{:.5f}, N_o:{:.5f}, dTheta:{:.5f}'.format(beta,N_t,N_c,N_o, suggested_change))
    output_file.write('\nSeed: {:.0f}'.format(seed))
    
    average_plaquette  = 0.
    VEV_average_plaquette = 0.
    
    for i in range(N_t):
        lattice, accept_prob = update(lattice, beta, suggested_change)
        print('{:.0f}/{:.0f}-Acceptance Probability: {:.3f}'.format(i+1,N_t,accept_prob))
    
    output_file.write('\nThermalisation complete')
    
    for i in range(N_o):
        output_file.write('\nMeasurement[{:.0f}]'.format(i))
        
        for j in range(N_c):
            lattice, accept_prob = update(lattice, beta, suggested_change)
        average_plaquette = average_plaq(lattice, beta)
        output_file.write('\nAverage Plaquette: {:.5f}'.format(average_plaquette))
        
        VEV_average_plaquette += average_plaquette
        print('{:.0f}/{:.0f}-Average Plaquette: {:.3f}'.format(i+1,N_o,average_plaquette))        
        
    VEV_average_plaquette = VEV_average_plaquette / N_o
    print('VEV average plaquette: {:.3f}'.format(VEV_average_plaquette))
    output_file.write('\nVEV Average Plaquette: {:.5f}'.format(VEV_average_plaquette))
    output_file.write('\nEND')
    output_file.close()