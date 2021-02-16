# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 14:19:27 2021

@author: David
"""
def update(lattice, beta, suggested_change, change_type = 'u'):
    #For each link in lattice suggest change in link and decide whether to accept it
    #Outputs acceptance probability and final lattice configuration
    
    #initialise variables
    current_ind = [0,0,0,0]
    accept_prob = 0.
    #Choose new link variables to add to the current state of the lattice
    lattice_size = (lattice.shape[0],lattice.shape[1],lattice.shape[2],lattice.shape[3],4)
    if change_type == 'n':
        lattice_change = np.random.normal(0., suggested_change, size = lattice_size)
    elif change_type == 'u': 
        lattice_change = np.random.uniform(low = -suggested_change , high = +suggested_change, size = lattice_size)
    else:
        lattice_change = suggested_change*np.sign(np.random.random(size = (lattice_size)) - 0.5)
    
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
                          #link_change =   np.random.normal(0., suggested_change)
                          #Alternative link_change = suggested_change * np.sign(np.random.rand() - 0.5)
                          
                          accept, S_change = change_link(lattice,beta,lattice_change[t,x,y,z,link_ind], current_ind, link_ind)
                          if(accept):
                              accept_prob += 1.
                          else:
                              lattice_change[t,x,y,z,link_ind] = 0.
    #accept_prob = Number of accepted changes / Total number of links
    for t in range(lattice.shape[0]):
        for x in range(lattice.shape[1]):
            for y in range(lattice.shape[2]):
                for z in range(lattice.shape[3]):
                    lattice[t,x,y,z].U1_angle += lattice_change[t,x,y,z,:] 
    accept_prob = accept_prob / (4 * lattice.shape[0]*lattice.shape[1]*lattice.shape[2]*lattice.shape[3])
    return lattice, accept_prob


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
    return accept, S_change

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

