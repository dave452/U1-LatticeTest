# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 20:04:26 2021

@author: David
"""
def action(lattice, beta):
    
def createLattice(Nt, Ns):
    lattice_size = (Nt + 2, Ns + 2, Ns + 2, Ns + 2, 4)
    lattice = 2*np.pi * (np.random.rand(lattice_size) - 0.5)
    
    edget, corrt = [0,Nt+1], [Nt,1]
    edges, corrs = [0,Ns+1], [Ns,0]
    
    pos = np.array([0,0,0,0])
    for t in range(lattice_size[0]):
        if(t == edget[0]):
            pos[0] = corrt[0]
        elif(t == edget[1]):
            pos[0] = corrt[1]
        else:
            pos[0] = t
            
        for x in range(lattice_size[1]):
            if(t == edget[0]):
                pos[1] = corrt[0]
            elif(t == edget[1]):
                pos[1] = corrt[1]
            else:
                pos[1] = t 
                
            for y in range(lattice_size[2]):
                pos[2] = y
                for z in range(lattice_size[3]):
                    pos[3] = z
    lattice[:,Nt+1, :, :, :] = lattice[:,1,:,:,:]
    lattice[:,0,:,:,:] = lattice[:,Nt,:,:,:]
    lattice[:,:,Ns+1, :, :] = lattice[:,:,1,:,:]
    lattice[:,:,0,:,:] = lattice[:,:,Ns,:,:]
    lattice[:,:,:,Ns+1, :] = lattice[:,:,:,1,:]
    lattice[:,:,:,0,:] = lattice[:,:,:,Ns,:]
    lattice[:,:,:,:,Ns+1] = lattice[:,:,:,:,1]
    lattice[:,:,:,:,0] = lattice[:,:,:,:,Ns]
    
    #
    lattice[:,Nt+1, Ns+1, :, :] = lattice[:,1,1,:,:]
    lattice[:,0,:,:,:] = lattice[:,Nt,:,:,:]
    
#NtNsNsNsNl  Nl - number of links per site, Nt - temporal size, Ns - spatial size 
Nt, Ns = 4, 4
V = Nt * (Ns**3)


print(lattice.shape)

