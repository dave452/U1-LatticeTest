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

def average_plaq(lattice):
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

def polykov_loop(lattice, start_ind):
    #Calculate and output the Polyakov loop
    move = np.array([1,0,0,0])
    current_ind = start_ind
    field_change = 0.
    polyakov = 0.
    for i in range(lattice.shape[0]):
        current_ind, field_change = moveOnLattice(lattice, current_ind, move, 0)
        polyakov += field_change
    polyakov = polyakov / lattice.shape[0]
    return polyakov

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
  
def change_link(lattice,beta, link_change, current_ind, link_ind, S, E, dE, a_i):
    #Decide whether to change link based on Boltzmann weight related to action due to selected link
    #Outputs whether the change is accepted, the change in the action, and the currect lattice configuration
    
    #Action due to a link in current configuration
    S_current = action_due_to_link(lattice, beta, current_ind, link_ind)
    
    #Change lattice and calculate the change in action due to change
    lattice[current_ind[0],current_ind[1],current_ind[2],current_ind[3]].U1_angle[link_ind] += link_change
    S_new = action_due_to_link(lattice, beta, current_ind, link_ind)
    S_change = S_new - S_current
    
    #Decide whether to accept the change to the lattice link
    activ_prob = np.exp(-a_i*S_change)
    accept = (np.random.rand() < activ_prob) and ((np.abs(S + S_change) <= np.abs(E+dE)) and (np.abs(S + S_change) >= np.abs(E)))
    if(not accept):       
        #revert changes if change not accepted
        S_change = 0
        lattice[current_ind[0],current_ind[1],current_ind[2],current_ind[3]].U1_angle[link_ind] -= link_change
    S += S_change
    return accept, S, lattice

def update(lattice, beta, suggested_change, S = 0., E = 0., dE = 10000., N_l = 1, a_i = 1):
    #For each link in lattice suggest change in link and decide whether to accept it
    #Outputs acceptance probability and final lattice configuration
    
    #initialise variables
    current_ind = [0,0,0,0]
    accept_prob = 0.
    link_change = 0.
    
    #For every link in the lattice
    for t in range(lattice.shape[0]):
        current_ind[0] =t
        for x in range(lattice.shape[1]):   
            current_ind[1] = x
            for y in range(lattice.shape[2]):   
                current_ind[2] = y
                for z in range(lattice.shape[3]): 
                    current_ind[3] = z
                    for link_ind in range(4):
                        for n in range(N_l):  
                          #Suggest change and decide whether to accept it
                          link_change = np.random.uniform(low = -suggested_change , high = +suggested_change)
                          #Alternative link_change = suggested_change * np.sign(np.random.rand() - 0.5)
                          accept, S, lattice = change_link(lattice,beta,link_change, current_ind, link_ind, S, E, dE, a_i)
                          if(accept):
                              accept_prob += 1.
    #accept_prob = Number of accepted changes / Total number of links
    accept_prob = accept_prob / (4 * N_l * lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3])
    return lattice, accept_prob, S



def create_lattice(lattice_size, seed = 0, test = False):
    #Randomly initialise lattice based on the seed and the lattice class
    #or use test configuration
    #output the lattice
    #print(seed)
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
    #initialise lattice
    lattice = create_lattice(lattice_size, seed = seed)
    
    #open output file and output system variables
    output_file = open(output_filename, 'a')
    output_file.write('\nBEGIN')
    output_file.write('\nLattice size: [{:.0f},{:.0f},{:.0f},{:.0f}]'.format(lattice_size[0], lattice_size[1],lattice_size[2],lattice_size[3]))
    output_file.write('\nBeta:{:.5f}, N_t:{:.5f}, N_c:{:.5f}, N_o:{:.5f}, dTheta:{:.5f}'.format(beta,N_t,N_c,N_o, suggested_change))
    output_file.write('\nSeed: {:.0f}'.format(seed))
    
    #initialise observables
    average_plaquette  = 0.
    VEV_average_plaquette = 0.
    average_accept_prob = 0.
    accept_prob = 0.

    #Thermalisation of the lattice
    for i in range(N_t):
        lattice, accept_prob, S = update(lattice, beta, suggested_change)
        print('{:.0f}/{:.0f}-Acceptance Probability: {:.3f}'.format(i+1,N_t,accept_prob))
        average_accept_prob += accept_prob
    #Thermalsation complete
    average_accept_prob = average_accept_prob / N_t
    output_file.write('\nThermalisation complete')
    output_file.write('\nAverage Acceptance Probability [{:.3f}]'.format(average_accept_prob))
    S = average_plaq(lattice) * (- 1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6))
    #Make N_o observations
    for i in range(N_o):
        output_file.write('\nMeasurement[{:.0f}]'.format(i))
        
        #Update the lattice N_c times (find new uncorrelated configuration)
        for j in range(N_c):
            lattice, accept_prob,S = update(lattice, beta, suggested_change, S = S)
        #Calculate and output average plaquette of current configuration
        average_plaquette = (S / (- 1. * beta * (lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3]*6)))
        output_file.write('\nAverage Plaquette: {:.5f}'.format(average_plaquette))
        print('{:.0f}/{:.0f}-Average Plaquette: {:.3f}'.format(i+1,N_o,average_plaquette))
        #Add current average plaquette to total average plaquette
        VEV_average_plaquette += average_plaquette
    
    #Find VEV average plaquette from total average plaquette and output results
    VEV_average_plaquette = VEV_average_plaquette / N_o
    print('VEV average plaquette: {:.3f}'.format(VEV_average_plaquette))
    output_file.write('\nVEV Average Plaquette: {:.5f}'.format(VEV_average_plaquette))
    
    #Close files
    output_file.write('\nEND')
    output_file.close()