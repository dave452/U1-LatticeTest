# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:14:17 2021

@author: David
"""

import numpy as np
import U1LatticeFunctions as U1
import U1LatticeTestFunctions as U1Test
#Defines a Lattice sizes  
#N = [Lattice Size Time, L.S x, L.S y, L.S z]

lattice_size = [4,4,4,4]
beta = np.array([0.95])
suggested_change = np.pi / 2.5
 # standard deviation of the change
N_t = 100 # thermalisation steps
N_c = 1 # number of steps between observations (assumed correlated)
N_o = 1000 # number of oberservations 
seed = np.array([100])
for i in range(beta.shape[0]):
    filename = './output/'+str(lattice_size[0])+str(lattice_size[1])+str(lattice_size[2])+str(lattice_size[3])+'b'+str(beta[i])+'s'+str(seed[i]) + '.txt'
    U1.main(lattice_size, beta[i], suggested_change, N_t, N_c, N_o, filename ,seed[i])
#U1Test.shapeOfLink(lattice_size)
#U1Test.test_action(lattice_size, beta)