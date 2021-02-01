# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 14:19:27 2021

@author: David
"""

def change_link(lattice,beta, link_change, current_ind, link_ind):
    #Decide whether to change link based on Boltzmann weight related to action due to selected link
    #Outputs whether the change is accepted, the change in the action, and the currect lattice configuration
    
    #Action due to a link in current configuration
    S_current = action_due_to_link(lattice, beta, current_ind, link_ind)
    
    #Change lattice and calculate the change in action due to change
    lattice[current_ind[0],current_ind[1],current_ind[2],current_ind[3]].U1_angle[link_ind] += link_change
    S_new = action_due_to_link(lattice, beta, current_ind, link_ind)
    S_change = S_new - S_current
    
    #Decide whether to accept the change to the lattice link
    activ_prob = np.exp(-S_change)
    accept = (np.random.rand() < activ_prob)
    if(not accept):
        #revert changes if change not accepted
        S_change = 0
        lattice[current_ind[0],current_ind[1],current_ind[2],current_ind[3]].U1_angle[link_ind] -= link_change
    return accept, S_change, lattice

def update(lattice, beta, suggested_change):
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
                          #Suggest change and decide whether to accept it
                          link_change =   np.random.normal(0., suggested_change)
                          #Alternative link_change = suggested_change * np.sign(np.random.rand() - 0.5)
                          
                          accept, S_change, lattice = change_link(lattice,beta,link_change, current_ind, link_ind)
                          if(accept):
                              accept_prob += 1.
    #accept_prob = Number of accepted changes / Total number of links
    accept_prob = accept_prob / (4 * lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3])
    return lattice, accept_prob 